const formCreateTweet = document.querySelector("[data-form=create-tweet]")
const buttonAddImage = formCreateTweet.querySelector("[data-action=add-image]")
const inputAddImage = formCreateTweet.querySelector("#tweet-image")
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
const buttonRemoveImage = document.querySelector("[data-action=remove-image]")

buttonAddImage.addEventListener("click", () => inputAddImage.click())
inputAddImage.addEventListener("change", handleTweetAddImage)
buttonRemoveImage.addEventListener("click", handleTweetRemoveImage)

function handleTweetAddImage() {
  const selectedFile = this.files[0]

  if (!selectedFile) return tweetImageContainer.classList.add("is-hidden")

  tweetImage.src = URL.createObjectURL(selectedFile)
  tweetImageContainer.classList.remove("is-hidden")
}

function handleTweetRemoveImage() {
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

  const { tweet_id: id, tweet_image_file_name: image_file_name, tweet_text: text } = await request.json()

  if (!request.ok) return alert("Could not tweet")

  tweetImageContainer.classList.add("is-hidden")
  tweetImage.src = ""
  form.reset()

  const template = templateTweetItem.content.cloneNode(true)
  template.querySelector("[data-form=tweet]").setAttribute("data-id", id)
  template.querySelector("[data-field=text]").textContent = text

  if (image_file_name) {
    template.querySelector("[data-field=image]").src = `static/tweets/${image_file_name}`
    template.querySelector("[data-field=image]").classList.remove("is-hidden")
  } else {
    template.querySelector("[data-field=image]").remove()
  }

  template.querySelector("[data-action=delete]").addEventListener("click", handleDeleteTweet)

  hookTweets.prepend(template)

  async function handleDeleteTweet() {
    const request = await fetch(`/tweets/${id}`, {
      method: "DELETE",
    })

    const response = await request

    if (!response.ok) return alert("Could not delete tweet")

    hookTweets.querySelector(`[data-form="tweet"][data-id="${id}"]`).remove()
  }
}
