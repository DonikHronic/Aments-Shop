$(function () {
	$('#shopping-cart').on('click', function () {
		$.get('/accounts/cart-api/').done(function (data) {
			let cart_modal = $('#modal_cart')
			let cart_item = ''
			for (let dataKey in data) {
				if (typeof (data[dataKey]) == "number") {
					$('#total-cart-price').text(`$${data[dataKey]}`)
					break
				}
				let price = data[dataKey]['product']['price'];
				if (data[dataKey]['product']['sales_price'].length === 2)
					price = data[dataKey]['product']['sales_price'][1];

				cart_item += `
					<li class="offcanvas-cart-item-single">
						<div class="offcanvas-cart-item-block">
							<a href="${data[dataKey]['product']['url']}" class="offcanvas-cart-item-image-link">
								<img src="${data[dataKey]['product']['preview']}" alt="" class="offcanvas-cart-image">
							</a>
							<div class="offcanvas-cart-item-content">
								<a href="${data[dataKey]['product']['url']}" class="offcanvas-cart-item-link">
									${data[dataKey]['name']}
								</a>
								<div class="offcanvas-cart-item-details">
									<span class="offcanvas-cart-item-details-quantity">${data[dataKey]['count']} x </span>
									<span class="offcanvas-cart-item-details-price">$${price}</span>
								</div>
							</div>
						</div>
						<div class="offcanvas-cart-item-delete text-right delete-item">
							<a href="accounts/cart/remove/${data[dataKey]['id']}" class="offcanvas-cart-item-delete">
								<i class="fa fa-trash-o"></i>
							</a>
						</div>
					</li>
				`
				cart_modal.html(cart_item);
			}
		});
	});
});