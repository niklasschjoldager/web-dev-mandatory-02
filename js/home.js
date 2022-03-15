const formCreateTweet = document.querySelector("[data-form=create-tweet]")
const buttonAddMedia = formCreateTweet.querySelector("[data-action=add-media]")
const inputAddMedia = formCreateTweet.querySelector("#tweet-media")
const templateTweet = document.querySelector("[data-template=tweet]")
const hookTweets = document.querySelector("[data-hook=tweets]")

formCreateTweet.addEventListener("submit", handleCreateTweet)
buttonAddMedia.addEventListener("click", () => inputAddMedia.click())

async function handleCreateTweet(event) {
  event.preventDefault()
  const form = event.target
  const request = await fetch("/tweets", {
    method: "POST",
    body: new FormData(form),
  })

  const { tweet_id: id, tweet_text: text } = await request.json()

  if (!request.ok) return alert("Could not tweet")

  const template = templateTweet.content.cloneNode(true)
  template.querySelector(`[data-field="id"]`).textContent = id
  template.querySelector(`[data-field="text"]`).textContent = text

  hookTweets.append(template)
}
