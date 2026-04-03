jQuery(document).ready(function($) {
    "use strict";

    // Initialize tabs
    $(function() {
        $("#tabs").tabs();
    });

    // Page loading animation
    $("#preloader").animate({
        'opacity': '0'
    }, 600, function() {
        setTimeout(function() {
            $("#preloader").css("visibility", "hidden").fadeOut();
        }, 300);
    });

    // Header background on scroll
    $(window).scroll(function() {
        var scroll = $(window).scrollTop();
        var box = $('.header-text').height();
        var header = $('header').height();

        if (scroll >= box - header) {
            $("header").addClass("background-header");
        } else {
            $("header").removeClass("background-header");
        }
    });

    // Testimonials carousel
    if ($('.owl-testimonials').length) {
        $('.owl-testimonials').owlCarousel({
            loop: true,
            nav: false,
            dots: true,
            items: 1,
            margin: 30,
            autoplay: false,
            smartSpeed: 700,
            autoplayTimeout: 6000,
            responsive: {
                0: { items: 1, margin: 0 },
                460: { items: 1, margin: 0 },
                576: { items: 2, margin: 20 },
                992: { items: 2, margin: 30 }
            }
        });
    }

    // Partners carousel
    if ($('.owl-partners').length) {
        $('.owl-partners').owlCarousel({
            loop: true,
            nav: false,
            dots: true,
            items: 1,
            margin: 30,
            autoplay: false,
            smartSpeed: 700,
            autoplayTimeout: 6000,
            responsive: {
                0: { items: 1, margin: 0 },
                460: { items: 1, margin: 0 },
                576: { items: 2, margin: 20 },
                992: { items: 4, margin: 30 }
            }
        });
    }

    // Modern slider
    if ($('.Modern-Slider').length) {
        $(".Modern-Slider").slick({
            autoplay: true,
            autoplaySpeed: 10000,
            speed: 600,
            slidesToShow: 1,
            slidesToScroll: 1,
            pauseOnHover: false,
            dots: true,
            pauseOnDotsHover: true,
            cssEase: 'linear',
            // fade: true, // commented out option
            draggable: false,
            prevArrow: '<button class="PrevArrow"></button>',
            nextArrow: '<button class="NextArrow"></button>',
        });
    }

    // Improved visibility check function
    function isElementInViewport(el) {
        var rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    function checkCounters() {
        $('.count-digit').each(function() {
            var $this = $(this);

            if (isElementInViewport(this) && !$this.hasClass('counter-loaded') && $this.is(':visible')) {
                $this.addClass('counter-loaded');

                var originalText = $this.text().trim();

                // Remove commas and any non-numeric characters except plus sign
                var cleanText = originalText.replace(/,/g, '').replace(/[^\d+]/g, '');

                // Extract the number (handle the + sign)
                var targetNumber = parseInt(cleanText) || 0;

                // Preserve the original format (comma and plus sign)
                var hasPlus = originalText.includes('+');

                // Store original values as data attributes
                $this.data('target', targetNumber);
                $this.data('hasPlus', hasPlus);

                // Start animation from 0
                $this.text('0' + (hasPlus ? '+' : ''));

                jQuery({
                    Counter: 0
                }).animate({
                    Counter: targetNumber
                }, {
                    duration: 3000,
                    easing: 'swing',
                    step: function() {
                        var currentValue = Math.ceil(this.Counter);
                        // Format number with commas
                        var formattedValue = currentValue.toLocaleString('en-US');
                        $this.text(formattedValue + (hasPlus ? '+' : ''));
                    },
                    complete: function() {
                        // Ensure final value is correctly formatted
                        var finalValue = targetNumber.toLocaleString('en-US');
                        $this.text(finalValue + (hasPlus ? '+' : ''));
                    }
                });
            }
        });
    }

    // Check counters on scroll and on load
    $(window).scroll(function() {
        checkCounters();
    });

    // Initial check when page loads
    setTimeout(function() {
        checkCounters();
    }, 500);
});