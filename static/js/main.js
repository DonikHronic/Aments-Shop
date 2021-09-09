(function ($) {
    "use strict";

    /*****************************
     * Commons Variables
     *****************************/
    let $body = $('body');

    /****************************
     * Sticky Menu
     *****************************/
    $(window).on('scroll', function () {
        let scroll = $(window).scrollTop();
        if (scroll < 100) {
            $(".sticky-header").removeClass("sticky");
        } else {
            $(".sticky-header").addClass("sticky");
        }
    });


    /*****************************
     * Off Canvas Function
     *****************************/
    (function () {
        let $offCanvasToggle = $('.offcanvas-toggle'),
            $offCanvas = $('.offcanvas'),
            $offCanvasOverlay = $('.offcanvas-overlay'),
            $mobileMenuToggle = $('.mobile-menu-toggle');
        $offCanvasToggle.on('click', function (e) {
            e.preventDefault();
            let $this = $(this),
                $target = $this.attr('href');
            $body.addClass('offcanvas-open');
            $($target).addClass('offcanvas-open');
            $offCanvasOverlay.fadeIn();
            if ($this.parent().hasClass('mobile-menu-toggle')) {
                $this.addClass('close');
            }
        });
        $('.offcanvas-close, .offcanvas-overlay').on('click', function (e) {
            e.preventDefault();
            $body.removeClass('offcanvas-open');
            $offCanvas.removeClass('offcanvas-open');
            $offCanvasOverlay.fadeOut();
            $mobileMenuToggle.find('a').removeClass('close');
        });
    })();


    /**************************
     * Offcanvas: Menu Content
     **************************/
    function mobileOffCanvasMenu() {
        let $offCanvasNav = $('.offcanvas-menu'),
            $offCanvasNavSubMenu = $offCanvasNav.find('.mobile-sub-menu');

        /*Add Toggle Button With Off Canvas Sub Menu*/
        $offCanvasNavSubMenu.parent().prepend('<div class="offcanvas-menu-expand"></div>');

        /*Category Sub Menu Toggle*/
        $offCanvasNav.on('click', 'li a, .offcanvas-menu-expand', function (e) {
            let $this = $(this);
            if ($this.attr('href') === '#' || $this.hasClass('offcanvas-menu-expand')) {
                e.preventDefault();
                if ($this.siblings('ul:visible').length) {
                    $this.parent('li').removeClass('active');
                    $this.siblings('ul').slideUp();
                    $this.parent('li').find('li').removeClass('active');
                    $this.parent('li').find('ul:visible').slideUp();
                } else {
                    $this.parent('li').addClass('active');
                    $this.closest('li').siblings('li').removeClass('active').find('li').removeClass('active');
                    $this.closest('li').siblings('li').find('ul:visible').slideUp();
                    $this.siblings('ul').slideDown();
                }
            }
        });
    }

    mobileOffCanvasMenu();


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
            generate_products += `
            <div class="product-default-single border-around">
                <div class="product-img-warp" data-id="` + datas[datasKey]['id'] + `">
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
                            <li class="add_to_cart">
                                <a href="" data-toggle="modal" data-target="#modalAddcart">
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
        let element = '#' + tag_id
        for (let i in commands_list) {
            if (command === commands_list[i])
                check = true;
        }

        if (check) {
            $.get('/get_products/', {filter: command}).done(function (datas) {
                $(element).html(generate_product(datas));
            });
        }
    }


    setTimeout(function () {
        $('.add_to_cart').click(function () {
            let id_par = $(this).parents('.product-img-warp');
            let id = id_par.attr('data-id');
            alert('ok');
            let url = '/accounts/cart/add/' + String(id);
            $.get(url).done(function (data) {
                console.log('success');
            });
        });
    }, 1000);


    $('.product_remove').on('click', function () {
        let id = $(this).attr('data-id');
        let url = '/accounts/cart/remove/' + String(id);
        $.get(url);
        $(this).parent('tr').remove();
    });

    /******************************
     * Hero Slider - [Single Grid]
     *****************************/
    $('.hero-area-wrapper').slick({
        arrows: false,
        fade: true,
        dots: true,
        easing: 'linear',
        speed: 2000,
    });

    /************************************************
     * Product Slider - Style: Default [4 Grid, 1 Row]
     ***********************************************/
    setTimeout(function () {
        $('.product-default-slider-4grids-1row').slick({
            arrows: true,
            infinite: false,
            slidesToShow: 4,
            slidesToScroll: 1,
            rows: 1,
            easing: 'ease-out',
            speed: 1000,
            prevArrow: '<button type="button" class="default-slider-arrow default-slider-arrow--left prevArrow"><i class="fa fa-angle-left"></button>',
            nextArrow: '<button type="button"  class="default-slider-arrow default-slider-arrow--right nextArrow"><i class="fa fa-angle-right"></button>',
            responsive: [

                {
                    breakpoint: 1200,
                    settings: {
                        slidesToShow: 3
                    }
                },
                {
                    breakpoint: 992,
                    settings: {
                        slidesToShow: 2,
                    }
                },
                {
                    breakpoint: 575,
                    settings: {
                        slidesToShow: 1,
                    }
                },
            ]
        });
    }, 1000)

    /************************************************
     * Company logo Slider
     ***********************************************/
    $('.company-logo-slider').slick({
        autoplay: true,
        infinite: true,
        arrows: false,
        slidesToShow: 4,
        slidesToScroll: 1,
        easing: 'linear',
        speed: 1000,
        responsive: [
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 4
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 3
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 2
                }
            }
        ]
    });
    /***********************************
     * Gallery - Horizontal
     ************************************/
    $('.product-large-image-horaizontal').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: true,
        asNavFor: '.product-image-thumb-horizontal'
    });
    $('.product-image-thumb-horizontal').slick({
        slidesToShow: 4,
        slidesToScroll: 1,
        focusOnSelect: true,
        arrows: true,
        asNavFor: '.product-large-image-horaizontal',
        prevArrow: '<button type="button" class="gallery-nav gallery-nav-horizontal gallery-nav-horizontal-left prevArrow"><i class="fa fa-angle-left"></i></button>',
        nextArrow: '<button type="button"  class="gallery-nav gallery-nav-horizontal gallery-nav-horizontal-right nextArrow"><i class="fa fa-angle-right"></i></button>',
        responsive: [
            {
                breakpoint: 1200,
                settings: {
                    slidesToShow: 3
                }
            },
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 2
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 3
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 2
                }
            }
        ]
    });


    /********************************
     *  Product Gallery - Image Zoom
     **********************************/
    $('.zoom-image-hover').zoom();

    /***********************************
     * Gallery - Single Slider
     ************************************/
    $('.product-large-image-single-slider').slick({
        slidesToShow: 4,
        slidesToScroll: 1,
        focusOnSelect: true,
        arrows: true,
        prevArrow: '<button type="button" class="gallery-nav gallery-nav-horizontal gallery-nav-horizontal-left prevArrow"><i class="fa fa-angle-left"></i></button>',
        nextArrow: '<button type="button"  class="gallery-nav gallery-nav-horizontal gallery-nav-horizontal-right nextArrow"><i class="fa fa-angle-right"></i></button>',
        responsive: [

            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 3,
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 2,
                    arrows: false,
                    autoplay: true,
                    infinite: true,
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    arrows: false,
                    autoplay: true,
                    infinite: true,
                }
            }
        ]
    });

    /***********************************
     * Modal  Quick View Image
     ************************************/
    $('.modal-product-image-large').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: true,
        asNavFor: '.modal-product-image-thumb'
    });
    $('.modal-product-image-thumb').slick({
        slidesToShow: 4,
        slidesToScroll: 1,
        asNavFor: '.modal-product-image-large',
        focusOnSelect: true,
        prevArrow: '<button type="button" class="gallery-nav gallery-nav-horizontal gallery-nav-horizontal-left prevArrow"><i class="fa fa-angle-left"></i></button>',
        nextArrow: '<button type="button"  class="gallery-nav gallery-nav-horizontal gallery-nav-horizontal-right nextArrow"><i class="fa fa-angle-right"></i></button>',
    });
    $('.modal').on('shown.bs.modal', function (e) {
        $('.modal-product-image-large, .modal-product-image-thumb').slick('setPosition');
        $('.product-details-gallery-area').addClass('open');
    });

    /***********************************
     * Blog - Slider
     ************************************/
    $('.blog-image-slider').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        focusOnSelect: true,
        arrows: true,
        prevArrow: '<button type="button" class="gallery-nav gallery-nav-horizontal gallery-nav-horizontal-left prevArrow"><i class="fa fa-angle-left"></i></button>',
        nextArrow: '<button type="button"  class="gallery-nav gallery-nav-horizontal gallery-nav-horizontal-right nextArrow"><i class="fa fa-angle-right"></i></button>',
    });

    /***********************************
     * Testimonial - Slider
     ************************************/
    $('.testimonial-slider').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        focusOnSelect: true,
        dots: true,
        arrows: false,
    });

    /************************************************
     * Nice Select
     ***********************************************/
    $('select').niceSelect();

    /************************************************
     * Price Slider
     ***********************************************/
    let slider_range = $("#slider-range")
    slider_range.slider({
        range: true,
        min: 0,
        max: 500,
        values: [75, 300],
        slide: function (event, ui) {
            $("#amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
        }
    });
    $("#amount").val("$" + slider_range.slider("values", 0) + " - $" + slider_range.slider("values", 1));


    /************************************************
     * Video  Popup
     ***********************************************/
    $('.video-play-btn').venobox();

    /************************************************
     * Scroll Top
     ***********************************************/
    $body.materialScrollTop();


})(jQuery);

