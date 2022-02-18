$("document").ready(function () {
    AOS.init();


    //Show toast messages
    $('.toast').toast('show');


    //Show and hide contact popup when link is clicked
    $('#show-contact-form').click(function () {
        $(".contact-form").css("display", "block");
        return false;
    });

    $('#hide-contact-form').click(function () {
        $(".contact-form").css("display", "none");
        return false;
    });


    //Scroll button visible after 300px
    //Scroll button hidden before 300px
    window.onscroll = function () { scrollButtonVisible(); };
    function scrollButtonVisible() {
        if ($('body,html').scrollTop() < 300) {
            $("#scroll-top-button").css("display", "none");
        } else {
            if ($('body,html').scrollTop() > 300) {
                $("#scroll-top-button").css("display", "block");
            }
        }
    }


    //When clicked, window will scroll to the top page
    $('#scroll-top-button').on("click", function () {
        window.scrollTo(0, 0);
    });
});