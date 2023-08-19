const flash = $(".error");

setTimeout(() => {
  flash.slideUp(500);
}, 4000);

const checkbox = $(".checkbox");
const choices = $(".choices");

choices.on("click", (evt) => {
  checkbox.prop("checked", false);
  choices.removeClass("select");

  if (evt.target.tagName === "LABEL") {
    evt.target.nextElementSibling.checked = true;
    $(evt.target.parentElement).addClass("select");
  } else {
    evt.target.children[1].checked = true;
    $(evt.target).addClass("select");
  }
});
