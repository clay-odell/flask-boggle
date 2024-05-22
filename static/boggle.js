let score = 0;
let clockMax = 15;
let timer = setInterval(countDown, 1000);
let words = new Set();
let board = $("#board");

function addTimerCountdown() {
  $(".timer").text(`Time Remaining: ${clockMax} seconds.`);
}

function userWordListAdd(word) {
  $(".user-list")
    .append($("<li>", { text: word }))
    .show();
}

function msgAppend(msg, cls) {
  $(".msg").text(msg).removeClass().addClass(`msg ${cls}`);
}

function scoreBoard() {
  $(".score").text(`Score: ${score} points`);
}

$(".word-submit").on("submit", async function (evt) {
  evt.preventDefault();
  const $word = $("#word-input");
  let word = $word.val();
  if (!word) return;

  if (words.has(word)) {
    $word.val("");
    msgAppend(`${word} can only be used once.`, "msg");
    return;
  }

  

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
    words.add(word);
    scoreBoard();
  }
  $word.val("");
});

async function countDown() {
  clockMax -= 1;
  addTimerCountdown();
  if (clockMax === 0) {
    $(".word-submit").hide();
    clearInterval(timer);
    $(".timer").hide();
    await postScore(score);

  }
}
async function postScore(score){
   const response = await axios.post("/post-score", {score: score});
   if (response.data.newRecord){
    msgAppend(`New Record: ${score}`, "msg");
    $(".highscore").text(`High Score: ${score}`);
    } else {
    msgAppend(`Final Score: ${score}`, "msg")
   }
}
