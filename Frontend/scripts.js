const sleep = ms => new Promise(r => setTimeout(r, ms));

var container;
var coords;
var names;
var center;

document.addEventListener("DOMContentLoaded", async function () {
    container = document.getElementById('places-holder');
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
        elem.classList.add("startanim-end");
    });

    await sleep(1000);

    // Hide the fullscreen blur cover
    $(".blur-cover").hide();
});


async function proceedToPage(num) {
    var page1 = $(`#page${num - 1}`);
    var page2 = $(`#page${num}`);

    // Show the second page before animating
    //$("#page2").show();

    // Move first page to the left
    page1.addClass("pageanim-end");
    // Move second page from the right
    page2.removeClass("pageanim-before");

    await sleep(1000);

    // Hide the first page out of frame
    page1.hide();
}

function sendImage() {
    let photo = document.getElementById("img-prompt").files[0];
    let city = document.getElementById("city").value;
    let formData = new FormData();

    formData.append("image", photo);
    formData.append("city", city);

    $.ajax({
        url: "http://127.0.0.1:5045/ai/places/img",
        data: formData,
        processData: false,
        contentType: false,
        type: "POST",
        success: function (data, textStatus, jqXHR) {
            console.log("out");
            console.log(data);
            fetchDetails(data);
        }
    });

    proceedToPage(3);
}

function fetchDetails(ids) {
    console.log(ids);
    $.ajax({
        url: "http://127.0.0.1:5008/places/get/batch",
        data: { ids: ids },
        traditional: true,
        type: "GET",
        success: function (data, status, jqXHR) {
            console.log(data);

            coords = [];
            names = [];

            data.forEach(place => {
                drawPlace(place.name, place.description, place.address);

                console.log(place);

                coords.push([place.longitude, place.latitude]);
                names.push(place.name);
            });

            center = coords[0];

            ymaps.ready(drawMap);
        }
    });
}

function sendText() {
    let text = document.getElementById("prompt").value;
    let city = document.getElementById("city").value;
    let formData = new FormData();

    formData.append("prompt", text);
    formData.append("city", city);

    $.ajax({
        url: "http://127.0.0.1:5045/ai/places/text",
        data: formData,
        processData: false,
        contentType: false,
        type: "POST",
        success: function (data, textStatus, jqXHR) {
            fetchDetails(data);
        }
    });


    proceedToPage(3);
}

function drawPlace(name, description, address) {
    const itemDiv = document.createElement('div');
    itemDiv.classList.add('place');

    itemDiv.innerHTML = `
        <p class="place-name">${name}</p>
        <p class="place-description">${description}</p>
        <p class="place-address">${address}</p>
    `;

    container.appendChild(itemDiv);
}

function drawMap() {
    var myMap = new ymaps.Map("map", {
        center: center,
        zoom: 10
    });
    const {YMapZoomControl} = ymaps3.import('@yandex/ymaps3-controls@0.0.1')
    ymaps.route(
        coords
    ).then(function (route) {
        myMap.geoObjects.add(route);

        var points = route.getWayPoints();

        for (var i = 0; i < names.length; i++) {
            points.get(i).properties.set('iconContent', names[i]);
        }

        points.options.set('preset', 'twirl#redStretchyIcon');
    });
}