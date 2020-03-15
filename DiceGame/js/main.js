window.onload = function startGame() {
    var firstTime = localStorage.getItem("first_time");
    if(!firstTime) {
    // first time loaded!
    localStorage.setItem("first_time","1");
}

else
{
    play_game()
}
}



function play_game() {
    var score1 = Math.floor(Math.random() * 6 + 1);
    var score2 = Math.floor(Math.random() * 6 + 1);

    if(score1 == score2)
    {
        heading_text = "Draw!";
        right_flag_class = ".hidden_flag col-1";
        left_flag_class = ".hidden_flag col-1";
    }

    if(score1 > score2)
    {
        heading_text = "Player 1 wins!";
        right_flag_class = ".visible_flag col-1";
        left_flag_class = ".hidden_flag col-1";
    }

    if(score1 < score2)
    {
        heading_text = "Player 2 wins!";
        right_flag_class = ".hidden_flag col-1";
        left_flag_class = ".visible_flag col-1";
    }

    img_class1 = "dice_img_" + score1;
    img_class2 = "dice_img_" + score2;

    document.querySelector("#dice_1").setAttribute("class", img_class1);
    document.querySelector("#dice_2").setAttribute("class", img_class2);

    document.querySelector(".heading").textContent = heading_text;

    document.querySelector("#flag_1").setAttribute("class", left_flag_class);
    document.querySelector("#flag_2").setAttribute("class", right_flag_class);
}