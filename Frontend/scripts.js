const sleep = ms => new Promise(r => setTimeout(r, ms));
document.addEventListener("DOMContentLoaded", async function () {
    var orlogobar = $("div.logobar:not(#alternative)");
    if (Math.random() < 0.05) {
        var logobar = $(".logobar");
        var altlogobar = $("#alternative.logobar");
        var altnavbar = $("#alternative.navbar");

        // Hide usual logo bar
        logobar.hide().css("opacity", "0%");
        // Show alternative logo bar
        altlogobar.show().css("opacity", "100%");

        await sleep(500);

        // Slowly hide alternative logobar text
        altnavbar.css("opacity", "0%");

        await sleep(500);

        // Display: none on alternative logobar text
        altnavbar.hide();
        // Move alternative logobar to the left
        altlogobar.css("left", "150%");

        await sleep(500);

        // Hide alternative logobar completely, move it to the top-left
        altlogobar.hide().css("left", "-5%").css("top", "5%").css("transition", "all 3s");
        // Also move usual logobar to the top-left and show it
        orlogobar.css("left", "-10%").css("top", "3%").show();

        await sleep(1);

        // Show alternative logobar and move it off the screen to the left
        altlogobar.show().css("left", "150%");
        // Hide the text on alternative logobar
        altnavbar.hide();
    }

    await sleep(199);

    // Fade in the original logobar
    orlogobar.show().css("opacity", "100%");

    // Reset the position on the original logobar
    orlogobar.css("left", "").css("top", "").show();

    // Show start animations
    var items = document.querySelectorAll(".startanim");
    items.forEach(elem => {
        elem.classList.add("end");
    });

    await sleep(1000);

    // Hide the fullscreen blur cover
    $(".blur-cover").hide();
});



function proceedToPage2() {
    $("#page1").hide();
    $("#page2").show();
}