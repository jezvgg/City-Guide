var timeout = 1000;

if (Math.random() <= 0.05) {
    document.addEventListener("DOMContentLoaded", function () {
        $(".logobar").hide().css("opacity", "0%");
        $("#alternative.logobar").show().css("opacity", "100%");
        timeout = 2200;
    });

    document.addEventListener("DOMContentLoaded", function () {
        setTimeout(function () {
            $(".navbar#alternative").css("opacity", "0%");
        }, 500)
    });

    document.addEventListener("DOMContentLoaded", function () {
        setTimeout(function () {
            $(".navbar#alternative").hide();
            $("#alternative.logobar").css("left", "150%");
            console.log("aaa");
        }, 1000)
    });

    document.addEventListener("DOMContentLoaded", function () {
        setTimeout(function () {
            $("div#alternative.logobar").hide().css("left", "-5%").css("top", "5%").css("transition", "all 3s");
            $("div.logobar:not(#alternative)").css("left", "-10%").css("top", "3%").show();
            console.log("aaa");
        }, 2000)
    });

    document.addEventListener("DOMContentLoaded", function () {
        setTimeout(function () {
            $("#alternative.logobar").show().css("left", "150%");
            $(".navbar#alternative").hide();
        }, 2001)
    });
}

document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        $(".logobar:not(#alternative)").show().css("opacity", "100%");

        $("div.logobar:not(#alternative)").css("left", "").css("top", "").show();

        $(".blur-cover").hide();

        var items = document.querySelectorAll(".startanim");
        items.forEach(elem => {
            elem.classList.add("end");
        });
    }, timeout);
});
