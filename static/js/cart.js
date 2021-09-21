$(function () {
	$('#shopping-cart').on('click', function () {
		$.get('/accounts/cart-api/').done(function (data) {
			let cart_modal = $('#modal_cart')
			let cart_item = ''
			for (let dataKey in data) {
				if (typeof (data[dataKey]) == "number") {
					console.log(data[dataKey]);
					$('#total-cart-price').text(`$${data[dataKey]}`)
					break
				}
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
									<span class="offcanvas-cart-item-details-quantity">1 x </span>
									<span class="offcanvas-cart-item-details-price">
										$${data[dataKey]['product']['price']}
									</span>
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
				console.log(data[dataKey]);
			}
		});
	});
});