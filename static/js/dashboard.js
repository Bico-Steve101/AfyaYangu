// Same as your previous dashboard.js
$(document).ready(function() {
    $(".reply-link").on("click", function(event) {
        event.preventDefault();
        var messageId = $(this).data("message-id");
        var replyFormContainer = $("#reply-form-container-" + messageId);

        if (messageId) {
            $.get("{% url 'Afya:reply_message' 999 %}".replace('999', messageId), function(data) {
                replyFormContainer.html(data);
                replyFormContainer.slideToggle();
            });
        }
    });
});
