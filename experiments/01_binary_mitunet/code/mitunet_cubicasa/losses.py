from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import nn

from .ontology import IGNORE_INDEX


class AsymmetricTverskyLoss(nn.Module):
    """Binary Tversky loss for raw logits."""

    def __init__(self, alpha: float = 0.6, beta: float = 0.4, gamma: float = 1.0, eps: float = 1e-7):
        super().__init__()
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.eps = eps

    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        targets = (targets > 0.5).to(dtype=logits.dtype)
        probs = torch.sigmoid(logits)
        dims = tuple(range(1, probs.ndim))
        tp = (probs * targets).sum(dim=dims)
        fp = (probs * (1 - targets)).sum(dim=dims)
        fn = ((1 - probs) * targets).sum(dim=dims)
        score = (tp + self.eps) / (tp + self.alpha * fp + self.beta * fn + self.eps)
        loss = (1 - score).pow(self.gamma)
        return loss.mean()


def multiclass_soft_dice_loss(
    logits: torch.Tensor,
    targets: torch.Tensor,
    ignore_index: int = IGNORE_INDEX,
    eps: float = 1e-6,
) -> torch.Tensor:
    if targets.ndim != 3:
        raise ValueError(f"Expected multiclass targets [B,H,W], got {tuple(targets.shape)}")
    if logits.ndim != 4:
        raise ValueError(f"Expected multiclass logits [B,C,H,W], got {tuple(logits.shape)}")
    if logits.shape[0] != targets.shape[0] or logits.shape[-2:] != targets.shape[-2:]:
        raise ValueError(f"Logits/targets shape mismatch: logits={tuple(logits.shape)} targets={tuple(targets.shape)}")
    num_classes = int(logits.shape[1])
    valid = targets != ignore_index
    safe_targets = targets.masked_fill(~valid, 0).long()
    probs = torch.softmax(logits, dim=1)
    one_hot = F.one_hot(safe_targets.clamp(0, num_classes - 1), num_classes=num_classes).permute(0, 3, 1, 2)
    one_hot = one_hot.to(dtype=probs.dtype)
    valid_mask = valid.unsqueeze(1).to(dtype=probs.dtype)
    probs = probs * valid_mask
    one_hot = one_hot * valid_mask
    dims = (0, 2, 3)
    intersection = (probs * one_hot).sum(dim=dims)
    cardinality = probs.sum(dim=dims) + one_hot.sum(dim=dims)
    present = cardinality > eps
    dice = (2.0 * intersection + eps) / (cardinality + eps)
    losses = 1.0 - dice
    if not bool(present.any()):
        return logits.sum() * 0.0
    return losses[present].mean()


class MultiHeadSegmentationLoss(nn.Module):
    def __init__(
        self,
        *,
        structure_ce_weight: float = 1.0,
        structure_dice_weight: float = 1.0,
        icon_ce_weight: float = 1.0,
        icon_dice_weight: float = 1.0,
        structure_task_weight: float = 1.0,
        icon_task_weight: float = 1.0,
        structure_class_weights: list[float] | None = None,
        icon_class_weights: list[float] | None = None,
        ignore_index: int = IGNORE_INDEX,
    ):
        super().__init__()
        self.structure_ce_weight = float(structure_ce_weight)
        self.structure_dice_weight = float(structure_dice_weight)
        self.icon_ce_weight = float(icon_ce_weight)
        self.icon_dice_weight = float(icon_dice_weight)
        self.structure_task_weight = float(structure_task_weight)
        self.icon_task_weight = float(icon_task_weight)
        self.ignore_index = int(ignore_index)
        self.register_buffer(
            "structure_class_weights",
            torch.tensor(structure_class_weights, dtype=torch.float32) if structure_class_weights is not None else None,
        )
        self.register_buffer(
            "icon_class_weights",
            torch.tensor(icon_class_weights, dtype=torch.float32) if icon_class_weights is not None else None,
        )

    def forward(self, outputs: dict[str, torch.Tensor], targets: dict[str, torch.Tensor]) -> dict[str, torch.Tensor]:
        structure_logits = outputs["structure"]
        icon_logits = outputs["icons"]
        structure_targets = targets["structure"].long()
        icon_targets = targets["icons"].long()
        structure_ce = F.cross_entropy(
            structure_logits,
            structure_targets,
            weight=self.structure_class_weights,
            ignore_index=self.ignore_index,
        )
        icon_ce = F.cross_entropy(
            icon_logits,
            icon_targets,
            weight=self.icon_class_weights,
            ignore_index=self.ignore_index,
        )
        structure_dice = multiclass_soft_dice_loss(structure_logits, structure_targets, ignore_index=self.ignore_index)
        icon_dice = multiclass_soft_dice_loss(icon_logits, icon_targets, ignore_index=self.ignore_index)
        structure_loss = self.structure_ce_weight * structure_ce + self.structure_dice_weight * structure_dice
        icon_loss = self.icon_ce_weight * icon_ce + self.icon_dice_weight * icon_dice
        total = self.structure_task_weight * structure_loss + self.icon_task_weight * icon_loss
        return {
            "loss": total,
            "structure_ce": structure_ce,
            "structure_dice_loss": structure_dice,
            "structure_loss": structure_loss,
            "icon_ce": icon_ce,
            "icon_dice_loss": icon_dice,
            "icon_loss": icon_loss,
        }
