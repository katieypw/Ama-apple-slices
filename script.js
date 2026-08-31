
/* =========================
   MAKE MESSAGES DRAGGABLE
========================= */

document.addEventListener("mousedown", function(event) {

  const message = event.target.closest(".floating-message");

  if (!message) return;


  message.classList.add("dragging");


  const page = document.querySelector(".page");

  const pageRect = page.getBoundingClientRect();

  const messageRect = message.getBoundingClientRect();


  const offsetX =
    event.clientX - messageRect.left;

  const offsetY =
    event.clientY - messageRect.top;


  function drag(event) {

    let x =
      event.clientX -
      pageRect.left -
      offsetX;

    let y =
      event.clientY -
      pageRect.top -
      offsetY;


    /* Keep message inside the yellow page */

    x = Math.max(
      0,
      Math.min(
        x,
        pageRect.width - messageRect.width
      )
    );

    y = Math.max(
      0,
      Math.min(
        y,
        pageRect.height - messageRect.height
      )
    );


    message.style.left =
      (x / pageRect.width * 100) + "%";

    message.style.top =
      (y / pageRect.height * 100) + "%";

  }


  function stopDragging() {

    message.classList.remove("dragging");

    document.removeEventListener(
      "mousemove",
      drag
    );

    document.removeEventListener(
      "mouseup",
      stopDragging
    );

  }


  document.addEventListener(
    "mousemove",
    drag
  );

  document.addEventListener(
    "mouseup",
    stopDragging
  );

});

