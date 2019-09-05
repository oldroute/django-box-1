
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


//Доп меню в футере
$('.arrow-img').click(function(){
    $(this).parent().find('ul').slideToggle();
    $(this).toggleClass('open');
    $(this).parent().parent().siblings('.menu__item ul').slideToggle();
});


