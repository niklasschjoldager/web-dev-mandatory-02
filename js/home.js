const formCreateTweet = document.querySelector("[data-form=create-tweet]")
const buttonAddMedia = formCreateTweet.querySelector("[data-action=add-media]")
const inputAddMedia = formCreateTweet.querySelector("#tweet-media")
const templateTweetItem = document.querySelector("[data-template=tweet-item]")
const hookTweets = document.querySelector("[data-hook=tweets]")

const tweetText = document.querySelector("[data-hook=tweet-text]")
initTweetTextResize()

function initTweetTextResize() {
  tweetText.style.height = `${tweetText.scrollHeight}px`
  tweetText.addEventListener("input", handleTweetTextResize)
}

function handleTweetTextResize() {
  this.style.height = ""
  this.style.height = `${this.scrollHeight}px`
}

const tweetImageContainer = document.querySelector("[data-hook=tweet-image-container]")
const tweetImage = document.querySelector("[data-hook=tweet-image]")
const buttonRemoveMedia = document.querySelector("[data-action=remove-media]")

buttonAddMedia.addEventListener("click", () => inputAddMedia.click())
inputAddMedia.addEventListener("change", handleTweetAddMedia)
buttonRemoveMedia.addEventListener("click", handleTweetRemoveMedia)

function handleTweetAddMedia() {
  const selectedFile = this.files[0]

  if (!selectedFile) return tweetImageContainer.classList.add("is-hidden")

  tweetImage.src = URL.createObjectURL(selectedFile)
  tweetImageContainer.classList.remove("is-hidden")
}

function handleTweetRemoveMedia() {
  tweetImage.src = ""
  tweetImageContainer.classList.add("is-hidden")
}

formCreateTweet.addEventListener("submit", handleCreateTweet)

async function handleCreateTweet(event) {
  event.preventDefault()
  const form = event.target
  const request = await fetch("/tweets", {
    method: "POST",
    body: new FormData(form),
  })

  const { tweet_id: id, tweet_text: text } = await request.json()

  if (!request.ok) return alert("Could not tweet")

  form.reset()

  const template = templateTweetItem.content.cloneNode(true)
  template.querySelector("[data-form=tweet]").setAttribute("id", id)
  template.querySelector("[data-field=text]").textContent = text

  hookTweets.prepend(template)
}
