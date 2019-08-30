

blockSitemapLoaded = () => {
    /** Карта сайта */
    $('.toggler').click(function() {
        $(this).closest('li').children('.inner').slideToggle(100)
        $(this).toggleClass('toggler-active')
    });
}

pageFrontpage = () => {

    // видео на главной
    var heroVideo = document.querySelector("video");
    if (heroVideo){
        heroVideo.play()
    }

    // эффекты радиального меню
    var logo = '#circle-logo',
        wave = '#circle-wave',
        menuSvg = 'circle-paths',
        menu = 'circle-menu',
        menuUl = '#circle-menu-ul',
        points = { start: 'circle-points-start', end: 'circle-points-end'},
        menuLi = { right: '.li__right', left: '.li__left'},
        startAngle = { right: 0, left: 180},
        xOffset = { right: 170, left: -170},
        menuCenter = { right: 90.0, left: 270.0},
        normK = { right: -1, left: 1},
        positionOffset = {right: 0, left: 150};

    var vMenu = '#vertical-menu',
        vWave = '#vertical-wave',
        vLogo = '#vertical-logo';

    drawPoint = function(key, key2, svg, rotateDeg, i){

        var div = document.createElement('div'),
            point = document.createElement('div');
        point.setAttribute('class', 'point')
        div.appendChild(point)
        div.style.transform = `rotate(${rotateDeg}deg)`
        document.getElementById(points[key2]).appendChild(div)
        return {
            x: point.getBoundingClientRect().left - svg.getBoundingClientRect().left,
            y: point.getBoundingClientRect().top - svg.getBoundingClientRect().top,
            d: rotateDeg
        }

    }

    createPointsContainer = function(){
        var _menu = document.getElementById(menu)
        var pointsStart = document.createElement('div')
        pointsStart.setAttribute('id', 'circle-points-start')
        pointsStart.setAttribute('class', 'circle__points start')
        _menu.appendChild(pointsStart)

        var pointsEnd = document.createElement('div')
        pointsEnd.setAttribute('id', 'circle-points-end')
        pointsEnd.setAttribute('class', 'circle__points end')
        _menu.appendChild(pointsEnd)
    }

    removePointsContainer = function(){
        var _menu = document.getElementById(menu)
        _menu.removeChild(document.getElementById(points['start']))
        _menu.removeChild(document.getElementById(points['end']))
    }

    getPathPoints = function(key, svg, item, i, rotateDeg, startAngle){
        p1 = drawPoint(key, 'start', svg, rotateDeg, i),
        p2 = drawPoint(key, 'end', svg, rotateDeg, i),
        p3 = {
            x: p2.x + xOffset[key],
            y: p2.y
        }
        return [p1, p2, p3]
    }

    drawPath = function(key, svg, i, points){

        var path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('id', `path-${key}-${i}`)
        path.setAttribute('d', `M ${points[0].x} ${points[0].y} L ${points[1].x} ${points[1].y} L ${points[2].x} ${points[2].y}`)
        svg.appendChild(path)

    }

    positionItem = function(key, i, points){
        var item = document.getElementById(`item-${key}-${i}`)
        item.style.left = points[1].x - positionOffset[key] + 'px'
        item.style.top = points[1].y - 87 + 'px'
    }

    normalizeHeight = function(key, points) {
        if(points.length > 4 && Math.abs(points[0][1].y - points[1][1].y) < 75) {

            var result = [],
                centerPointNum = null,
                minDiff = 180;

            for(var i=0; i < points.length; i++){
                var diff = Math.abs(menuCenter[key] - points[i][1].d)
                if(diff < minDiff){
                    centerPointNum = i
                    minDiff = diff
                }
            }

            for(var i=0; i < points.length; i++){
                points[i][1].s = Math.abs(i - centerPointNum)
            }

            if(centerPointNum != null){
                for(var i=0; i < points.length; i++){
                    let offset = 0
                    if(i < centerPointNum){
                        offset = points[i][1].s * 75.0 * normK[key]
                    } else if(i > centerPointNum){
                        offset = points[i][1].s * 75.0 * (- normK[key])
                    }
                    points[i][1].y = points[centerPointNum][1].y + offset
                    points[i][2].y = points[centerPointNum][2].y + offset
                }
            }
        }
        return points
    }

    createMenu = function(key){
        var items = document.querySelectorAll(menuLi[key]),
            stepDeg = 140 / items.length,
            points = [],
            svg = document.getElementById(menuSvg),
            sta = startAngle[key] + stepDeg * 0.5 + 20;

        for(var i = 0; i < items.length; i++) {
            var rotateDeg = sta + i * stepDeg
            points.push(getPathPoints(key, svg, items[i], i, rotateDeg, startAngle[key]))
        }
        points = normalizeHeight(key, points)
        points.forEach((points, index) => {
            drawPath(key, svg, index, points)
            positionItem(key, index, points)
        })
    }

    startMenu = function(){

        createPointsContainer()
        createMenu('left')
        createMenu('right')
        removePointsContainer()

    }

    checkWindowWith = function(){

        /** Инициализация циркулярного меню только один раз и только в десктоп/планшет разрешении */
        if(window.innerWidth > 767){
            if (!document.getElementById(menuSvg).hasChildNodes()){
                startMenu()
            }
        }
    }

    window.addEventListener("resize", (event) => checkWindowWith() );
    checkWindowWith()
    document.getElementById(menu).style.opacity = 1
    document.getElementById('vertical-logo').style.opacity = 0.6

    /* Эффекты десктопного меню  */
    var allAnimations = 'watch focus focusout focusout-watch'

    function logoClickHandler(){
        $(menuUl).toggleClass('active')
        $(wave).removeClass(allAnimations)

        if($(menuUl).hasClass('active')){
           // Меню открывается
            $(menuUl).find('li').removeClass("inactive")
            setTimeout(() => {
                $(menuUl).find('li').addClass("active")
                $(wave).addClass("focusout")
            } , 10)
        } else {
            // Меню закрывается
            $(menuUl).find('li').removeClass("active")
            setTimeout(() => {
                $(menuUl).find('li').addClass("inactive")
                $(wave).addClass("focus")
            } ,10)
        }
    }

    // Анимирование логотипа при наведении
   function logoMouseEnterHandler(){
       if(!$(menuUl).hasClass('active')){
            $(wave).removeClass(allAnimations);
            setTimeout(() => $(wave).addClass("focus") ,1)
        }
    }

    // Анимирование логотипа при потере фокуса мыши
   function logoMouseLeaveHandler(){
       if(!$(menuUl).hasClass('active')){
            $(wave).removeClass(allAnimations);
            setTimeout(() => $(wave).addClass("focusout-watch") ,1)
        }
    }

    // Анимирование пункта при наведении
    $('#circle-menu-ul').find('li').each(function(){
        $(this).on('mouseenter', () => {
          if($('#circle-menu-ul').hasClass('active')){
            let pathId = $(this).attr('data-path')
            $(pathId).addClass('active')
          }
        })

        $(this).on('mouseleave', () => {
            if($('#circle-menu-ul').hasClass('active')){
                $('#circle-paths path').removeClass('active')
            }
        })

    })

    $("body").on('click', logo, logoClickHandler)
    $("body").on('mouseenter', logo, logoMouseEnterHandler)
    $("body").on('mouseleave', logo, logoMouseLeaveHandler)

    /* Эффекты мобильного меню  */

    function vLogoClickHandler(){
        $(vMenu).toggleClass('active')
        $(vWave).removeClass('watch focus focusout focusout-watch');

        if($(vMenu).hasClass('active')){
            // Меню открывается
            var items = $(vMenu).find('a')
            var menuHeight = items.length * (items.first().outerHeight(true))
            $(vMenu).css('height', menuHeight + 'px')
        } else {
            // Меню закрывается
            $(vMenu).css('height', '0px')
            $(vWave).addClass("watch");
        }
    }


    $("body").on('click', vLogo, vLogoClickHandler)
}

pageCatalog = () => {

    //Слайдменю в каталоге

    $('.section__arrow').click(function(){
        var parent = $(this).parent()
        parent.toggleClass('active')

        parent.find('.section__line, .section__arrow').toggleClass('active');
        parent.find('.section__line').each(function(){
            if ($(this).hasClass('active')){
                var height = $(this).find('a').length * 24 + 'px'
                $(this).css('height', height)
            } else {
                $(this).css('height', '0px')
            }

        })

    });
}