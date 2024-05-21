let score = 0;

function userWordListAdd(word){
   $(".user-list").append($("<li>", {text: word})).show();
}

function msgAppend(msg, cls) {
  $(".msg").text(msg).removeClass().addClass(`msg ${cls}`);
}

function scoreBoard() {
  $(".score").text(`Player Score: ${score} points`);
}

$(".word-submit").on("submit", async function (evt) {
  evt.preventDefault();
  const word = $("#word-input").val();
  const resp = await axios.get("/word-submit", { params: { word: word } });
  let msgResult = resp.data.result;
  if (msgResult === "not-word") {
    msgAppend(`${word} is not a valid word. Please try again.`, "err");
  } else if (msgResult === "not-on-board") {
    msgAppend(
      `${word} is a word, but it isn't valid on this board. Please try again.`,
      "err"
    );
  } else {
    userWordListAdd(word);
    msgAppend(`Congrats! ${word} is a valid word`, "success");
    score += word.length;
    scoreBoard();
   }
  
});
