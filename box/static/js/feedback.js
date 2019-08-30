
// Google капчи и feedback
captchas = {
    'id-call-captcha': false,
    'id-callback-captcha': false,
    'id-service-captcha': false,
    'id-order-captcha': false,
}

feedback = {
    submit: function($form){
        var data = {};
        var form_array = $form.serializeArray();
        for (i = 0; i < form_array.length; i++){
            data[form_array[i].name] = form_array[i].value;
        }
        $.post($form.attr('action'), data, function(data, textStatus){
            $form.replaceWith(data).show();
            $('.important-field').hide();

        });
        return false;
    }
};

// ajax-отправка фос
$(document).on('submit', '.feedback-form', function(e){
    e.preventDefault();
    feedback.submit($(this));
});

// Рендеринг капч по открытию попап
$(document).on('click', '#id-call' , function(e){
    captchas['id-call-captcha'] = true
})

$(document).on('click', '#id-callback' , function(e){
    captchas['id-callback-captcha'] = true
})

$(document).on('click', '#id-service' , function(e){
    captchas['id-service-captcha'] = true
})

$(document).on('click', '#id-order' , function(e){
    captchas['id-order-captcha'] = true
})


captchaReady = () => {

    for (key in captchas){
        var el = document.getElementById(key);
        if( el ){
            grecaptcha.render(el, {'sitekey': el.getAttribute('data-sitekey'), 'theme': 'dark' });
            captchas[key] = true;
        }
    }
}

captchaWidgetLoaded = () => {

    /** Рендеринг видимых на странице капч */

    let captcha = document.querySelectorAll('.g-recaptcha')

    $('.g-recaptcha').each(function(){
        var captcha_id = $(this).attr('id');
        if(captchas[captcha_id] === true){
            var el = document.getElementById(captcha_id);
            try {
                grecaptcha.render(el, { 'sitekey': el.getAttribute('data-sitekey'), 'theme': 'dark' });
            } catch (err){ }
        } else {
            captchas[captcha_id] = false;
        }
    })
}