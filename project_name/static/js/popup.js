$('.mfp-open').magnificPopup({
    callbacks: {
                open: function() {
                    $('html').addClass('mfp-feedback mfp-opened');
                    $('body').addClass('noscroll')
                },
                close: function() {
                    $('html').removeClass('mfp-feedback mfp-opened');
                    $('body').removeClass('noscroll')
                }
            },
     });     




//Фотогалерея
$('.mfp-gallery').each(function() {
    $(this).magnificPopup({
        type: 'image',
        image: {
            cursor: null,
            tClose: 'Закрыть',
            titleSrc: function(item) {
                return item.img.attr('alt');
            }
        },
        gallery: {
            enabled: true,
            preload: [0, 2],
            navigateByImgClick: true,
            tPrev: 'Предыдущее фото',
            tNext: 'Следующее фото'
        },
        delegate: 'a[href$=".png"][target!="_blank"], \
					   a[href$=".PNG"][target!="_blank"], \
					   a[href$=".jpeg"][target!="_blank"], \
					   a[href$=".JPEG"][target!="_blank"], \
					   a[href$=".jpg"][target!="_blank"], \
					   a[href$=".JPG"][target!="_blank"]',
        callbacks: {
            buildControls: function() {
                if (this.items.length > 1) {
                    this.contentContainer.append(this.arrowLeft.add(this.arrowRight));
                }
            },
            open: function() {
                $('html').addClass('mfp-opened');
            },
            close: function() {
                $('html').removeClass('mfp-opened');
            }
        },
        closeMarkup: '<button title="Закрыть (ESC)" type="button" class="mfp-close"></button>',
    });
});

