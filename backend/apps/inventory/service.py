from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import transaction
from django.db.models import F

from apps.inventory.models import Product, StockHistory

if TYPE_CHECKING:
    from apps.core.models import User


def adjust_stock(
    *,
    product: Product,
    change: int,
    reason: StockHistory.ReasonChoices,
    user: User | None = None,
) -> StockHistory:
    """Adjusts product stock and records a StockHistory entry."""
    with transaction.atomic():
        # Update quantity atomically at DB level
        Product.objects.filter(pk=product.pk).update(quantity=F("quantity") + change)

        # Refresh instance if caller needs updated quantity
        product.refresh_from_db(fields=["quantity"])

        history: StockHistory = StockHistory.objects.create(
            product=product,
            change=change,
            reason=reason,
            performed_by=user,
        )

    return history
