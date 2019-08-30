
// Кнопка наверх
let buttonUp = document.querySelector('.btn__up')
if (buttonUp != undefined){
    buttonUp.addEventListener('click', function(){ $('html, body').animate( { scrollTop: 0 }, 700 ) })
    toggleButtonUp = () =>  (buttonUp != null && document.documentElement.scrollTop > 400) ? buttonUp.classList.add('btn__up--active') : buttonUp.classList.remove('btn__up--active')
    toggleButtonUp()
    window.onscroll = () => toggleButtonUp()
}

// маска телефона в форме
$(document).on('focus', 'input[name*="phone"]', function() {
	$(this).mask('+7(999)999-99-99',{placeholder:'+7(___)___-__-__'})
})

// Тоглеры
$('.toggler').click(function() {
    $(this).closest('li').children('.inner').slideToggle(100)
    $(this).toggleClass('toggler-active')
});

//Hamburger Menu

$('.hamburger, .menu__close').click(function() {
	$('.hamburger').toggleClass('active');
	$('.header__menu').toggleClass('active');

});

//Доп меню
$('.submenu-img').click(function(){
	$(this).parent().parent().find('.submenu').slideToggle();
	$(this).toggleClass('open');
});


//Обрезаем описание
function truncateWords(element, height) {
    var target;

    target = document.querySelectorAll(element);

    target.forEach(function(item) {
        var target_text, target_words;

        target_text = item.innerText;
        target_words = target_text.split(' ');

        if ((item.clientHeigth || item.offsetHeight) > height) {
            while ((item.clientHeigth || item.offsetHeight) > height) {
                target_words.pop();
                target_text = target_words.join(' ');
                item.innerText = target_text;
            }

            target_words = target_text.split(' ');
            target_words.pop();
            target_words.push('...');
            target_text = target_words.join(' ');
            item.innerText = target_text;
        }
    });
}

truncateWords('.card__description--oversize', 53);

// Правка бага карточки товара вставки ссылки в ссылку. Создает ссылку на производителя
var produsers = document.querySelectorAll('.card__produser');
[].forEach.call(produsers, function(produser) {
    var a = document.createElement('a')
    a.setAttribute('href', produser.getAttribute('data-href'))
    a.innerHTML = produser.textContent.trim()
    produser.innerHTML = ''
    produser.appendChild(a)
})

//Grid галерея фотографий 
let items = $(".gallery");
for (let i = 0; i < items.length; i++) {

    let countPhoto = $(items[i]).find('.gallery__item').length;
    if (countPhoto <= 4) {
        $(items[i]).addClass('little__gallery')
    }

}


// СЛАЙДЕР НА СТРАНИЦЕ ТОВАРА
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
//Фиксированное меню
$(window).on("scroll", function() {
    if ($(window).scrollTop() >= 200) {
        $('.header').addClass('fixed');
        if(window.innerWidth > 767){
            $('.wrapper').css('padding-top', '123px');
        } else {
            $('.wrapper').css('padding-top', '76px');
        }
        $('.logo__img, .logo__desc').hide();
        $('.logo__sticky').show();
    }
    else {
        $('.header').removeClass('fixed');
        $('.wrapper').css('padding-top', '0');
        $('.logo__img, .logo__desc').show();
        $('.logo__sticky').hide();
    }
});


//Доп меню в футере
$('.arrow-img').click(function(){
    $(this).parent().find('ul').slideToggle();
    $(this).toggleClass('open');
    $(this).parent().parent().siblings('.menu__item ul').slideToggle();
});


// Блок страницы по всей ширине если сайдбар пуст
var sidebar = document.querySelector('.right-column')
var leftCol = document.querySelector('.left-column')
if (leftCol != null){
    if (sidebar == null || sidebar.childElementCount == 0) {
        leftCol.style.width = '100%'
    }
}


// Позиционирование таблиц по ширине
var resize_handler = function(){
    if (leftCol){
        document.querySelectorAll('table').forEach((elem, index) => {
            var tbody = elem.querySelector('tbody')
            if (tbody && tbody.getBoundingClientRect().width < leftCol.getBoundingClientRect().width){
                elem.style.display = 'table'
            }
        })
    }
}
resize_handler()
window.addEventListener('resize', resize_handler)

// Прописывание заголовка страницы в мобильную версию
try {
    document.querySelector('.page__title.mobile h1').innerHTML = document.querySelector('.page__title.desktop h1').textContent
} catch {}

// Авторасчет высоты выпадающего списка разделов страницы каталога (мобильной)


/*

//Показать и скрыть контент
(function($) {
    var defaults = {
        minimal: 200,
        controls: ['<span>Читать далее</span>', '<span>Скрыть</span>'],
        speed: 500,
        scroll: false,
    };

    var options;

    $.fn.slidable = function(params) {
        var options = $.extend({}, defaults, params);
        var controller_html = '<div class="controller more">' +
            '<span>' + options.controls[0] + '</span>' +
        '</div>';

        function noHeightData(block) {
            return !$(block).data('height');
        }

        function switchController(controller) {
            var text = $(controller).hasClass('more') ? options.controls[1] : options.controls[0];
            
            setTimeout(function() {
                $(controller).html("<span>" + text + "</span>");
                $(controller).toggleClass('more');
                $(controller).toggleClass('less');

                if (options.scroll) {
                    controller.onclick = function() {
                        if ( $(this).hasClass('less') ) {
                            var destination = $(this).siblings('.tall').offset().top;
                            $('html, body').animate({
                                scrollTop: destination
                            }, options.speed);
                        }
                    }
                }
            }, options.speed);
        }

        function controllerAction() {
            var self = this;
            var block = $(self).siblings('.tall');
            var new_height = $(self).hasClass('more') ? block.data('height') : options.minimal;
            block.animate({
                height: new_height
            }, options.speed, switchController(self));
        }

        function handleClick(controller) {
            $(controller).on('click', controllerAction);
        }

        function init(slidable) {
            $(slidable).children('.tall').each(function() {
                var block = this,
                    height = block.clientHeight;
                if (noHeightData(block) && height > options.minimal) {
                    $(block).after(controller_html);
                    var controller = $(slidable).children('.controller');
                    handleClick(controller);
                    $(block).data('height', height);
                    $(block).height(options.minimal);
                }
            });
        }

        this.each(function() {
            init(this);
        });

        return this;
    };
})(jQuery);
// Сброс Slidable
function resetSlidable(target) {
    $(target+'.slidable > .tall').each(function() {
        var height = $(this).data('height');
        if (height) {
            $(this).css({'height': ''});
            $(this).removeData('height')
        }
    });
    $(target+'.slidable > .controller').each(function(){
        $(this).remove();
    });
}


$(function() {
    // СКРЫТИЕ ТЕКСТА КОНТЕНТА
    function contentSlidable(windowWidth) {
        resetSlidable('.page__content');
        if (windowWidth < 12768){
            $('.page__content.slidable').each(function(){
                $(this).slidable({
                    minimal: 50,
                    scroll: true,
                });
            });
        }
    }
   contentSlidable();
});

*/
