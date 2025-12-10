import pytest
from apps.inventory.models import Product, Supplier, StockHistory
from apps.sales.models import Sale, Customer
from apps.core.models import User, Employee

@pytest.mark.django_db
def test_sale_decrements_stock() -> None:
    supplier = Supplier.objects.create(name="Acme")
    user = User.objects.create(username="testuser")
    employee = Employee.objects.create(user=user)

    product = Product.objects.create(name="Widget", quantity=10, price="5.00", supplier=supplier)
    customer = Customer.objects.create(name="John")
    
    Sale.create_sale(product=product, customer=customer, employee=employee, quantity=3, total_price=15.00)

    product.refresh_from_db()
    assert product.quantity == 7
    assert StockHistory.objects.filter(product=product, change=-3).exists()


@pytest.mark.django_db
def test_sale_fails_on_insufficient_stock() -> None:
    user = User.objects.create(username="testuser2")
    employee = Employee.objects.create(user=user)

    product = Product.objects.create(name="Low", quantity=2, price="1.00")
    customer = Customer.objects.create(name="Buyer")

    with pytest.raises(ValueError):
        Sale.create_sale(
            product=product,
            customer=customer,
            employee=employee,
            quantity=5,
            total_price=5.00,
        )

    product.refresh_from_db()
    assert product.quantity == 2
