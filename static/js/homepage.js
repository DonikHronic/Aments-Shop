$(function () {
    let commands_list = []
    $(window).load(function () {
        $.get('/get_filter_list/').done(function (data) {
            let commands = JSON.parse(data)
            commands_list.push(...commands)
            getProducts("new_deliveries", "new_products");
            getProducts("popular_product", "popular_products");
        });
        $.get('/get_popular_categories/').done(function (data) {
            let in_block = $('#categories');
            let html = '';
            for (let dataKey in data) {
                html += `
                    <div class="col-lg-3 col-md-4 col-sm-6 col-12">
                        <!-- Start Product Catagory Single -->
                        <a href="` + data[dataKey]['url'] + `" class="product-catagory-single">
                            <div class="product-catagory-img">
                                <img src="` + data[dataKey]['category_image'] + `" alt="">
                            </div>
                            <div class="product-catagory-content">
                                <h5 class="product-catagory-title">` + data[dataKey]['name'] + `</h5>
                                <span class="product-catagory-items">(` + data[dataKey]['category_count'] + ` items)</span>
                            </div>
                        </a> <!-- End Product Catagory Single -->
                    </div>
                `
            }
            in_block.append(html)
        });
    });

    function generate_product(datas) {
        let generate_products = '';
        for (let datasKey in datas) {
            let product_price = 0

            if (datas[datasKey]['sales_price'].length === 2) {
                product_price = `
                    <del class="product-default-price-off">$ ` + datas[datasKey]['sales_price'][0] + `</del>
                    &nbsp;&nbsp;$ ` + datas[datasKey]['sales_price'][1] + `
                `
            } else {
                product_price = '$' + String(datas[datasKey]['sales_price'])
            }
            generate_products += `<div class="product-default-single border-around">
                <div class="product-img-warp">
                    <a href="` + datas[datasKey]['url'] + `" class="product-default-img-link">
                        <img src="` + datas[datasKey]['preview'] + `" alt="" class="product-default-img img-fluid">
                    </a>
                    <div class="product-action-icon-link">
                        <ul>
                            <li><a href="wishlist.html"><i class="icon-heart"></i></a></li>
                            <li><a href="compare.html"><i class="icon-repeat"></i></a></li>
                            <li>
                                <a href="#" data-toggle="modal" data-target="#modalQuickview">
                                    <i class="icon-eye"></i>
                                </a>
                            </li>
                            <li>
                                <a href="#" data-toggle="modal" data-target="#modalAddcart">
                                    <i class="icon-shopping-cart"></i>
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
                <div class="product-default-content">
                    <h6 class="product-default-link">
                        <a href="` + datas[datasKey]['url'] + `">` + datas[datasKey]['name'] + `</a>
                    </h6>
                    <span class="product-default-price">` + product_price + `</span>
                </div>
            </div>`
        }
        return generate_products;
    }

    function getProducts(command, tag_id) {
        let check = false;
        let id = '#' + tag_id
        for (let i in commands_list) {
            if (command === commands_list[i])
                check = true;
        }

        if (check) {
            $.get('/get_products/', {filter: command}).done(function (datas) {
                $(id).append(generate_product(datas));
            });
        }
    }

});