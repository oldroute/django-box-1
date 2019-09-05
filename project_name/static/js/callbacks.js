

blockSitemapLoaded = () => {
    /** Карта сайта */
    $('.toggler').click(function() {
        $(this).closest('li').children('.inner').slideToggle(100)
        $(this).toggleClass('toggler-active')
    });
}


pageProduct = () => {

    // слайдер
    let itemSliderFor = $('.item__slider-for')
    let itemSliderNav = $('.item__slider-nav')

    itemSliderFor.slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: true,
        dots: false,
        asNavFor: '.item__slider-nav'
    });
    //скрывать слайдер пока он не будет инициализирован
    if (itemSliderFor.hasClass('slick-initialized')) {
        itemSliderFor.css('display', 'block')
        itemSliderNav.css('display', 'flex')
    }

    //Адаптация нижнего слайдера на странице товара в зависимсоти от колличества изображений
    let itemNav = itemSliderNav.find('.item__slide').length;
    if ( itemNav > 1 && itemNav < 3 ) {
        itemSliderNav.slick({
            slidesToShow: 3,
            arrows: true,
            slidesToScroll: 1,
            asNavFor: '.item__slider-for',
            dots: false,
            centerMode: false,
            focusOnSelect: true,
        });
    } else if ( itemNav >= 3  ) {
        itemSliderNav.slick({
            slidesToShow: 3,
            arrows: true,
            slidesToScroll: 1,
            asNavFor: '.item__slider-for',
            dots: false,
            centerMode: true,
            focusOnSelect: true,
        });
        if ( itemNav >= 3 ) {
            itemSliderNav.find('.slick-list').addClass('slick-list--center');
        } else {null}

    } else {
        itemSliderNav.css('display', 'none');
    }

}