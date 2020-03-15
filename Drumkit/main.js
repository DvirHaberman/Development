buttonArray = document.querySelectorAll("button");

for (var i=0; i<buttonArray.length ; i++){
    buttonArray[i].addEventListener("click", handleClick);
}
function handleClick(){
    button = this.innerHTML;
    switch (button) {
        case "w":
          (new Audio('./sounds/crash.mp3')).play();
          break;
        case "a":
          (new Audio('./sounds/kick-bass.mp3')).play();
          break;
        case "s":
          (new Audio('./sounds/snare.mp3')).play();
          break;
        case "d":
          (new Audio('./sounds/tom-1.mp3')).play();
          break;
        case "j":
          (new Audio('./sounds/tom-2.mp3')).play();
          break;
        case "k":
          (new Audio('./sounds/tom-3.mp3')).play();
          break;
        case "l":
          (new Audio('./sounds/tom-4.mp3')).play();
          break;
        default:
          console.log(key);
      }

    button.getAttribute("class",this.innerHTML + "pressed");

}

function playSound(event) {
    key = event.key;
    switch (key) {
      case "w":
        (new Audio('./sounds/crash.mp3')).play();
        break;
      case "a":
        (new Audio('./sounds/kick-bass.mp3')).play();
        break;
      case "s":
        (new Audio('./sounds/snare.mp3')).play();
        break;
      case "d":
        (new Audio('./sounds/tom-1.mp3')).play();
        break;
      case "j":
        (new Audio('./sounds/tom-2.mp3')).play();
        break;
      case "k":
        (new Audio('./sounds/tom-3.mp3')).play();
        break;
      case "l":
        (new Audio('./sounds/tom-4.mp3')).play();
        break;
      default:
        console.log(key);
    }
  }

  addEventListener("keydown", playSound);