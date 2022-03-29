import Dropdown from "./classes/dropdown.js"
import Modal from "./classes/modal.js"

/**********************************/
// Create tweet
const formCreateTweet = document.querySelector("[data-form=create-tweet]")
formCreateTweet.addEventListener("submit", handleCreateTweet)
/**********************************/
/**********************************/
/**********************************/
const hookTweets = document.querySelector("[data-hook=tweets]")

const templateTweetItem = document.querySelector("[data-template=tweet-item]")

const modalEditTweet = document.querySelector("[data-modal=edit-tweet]")
const modalDeleteTweet = document.querySelector("[data-modal=delete-tweet]")

initTweetTextResize()

function initTweetTextResize() {
  const tweetText = document.querySelector("[data-hook=tweet-text]")
  tweetText.style.height = `${tweetText.scrollHeight}px`
  tweetText.addEventListener("input", handleTweetTextResize)
}

function handleTweetTextResize() {
  this.style.height = ""
  this.style.height = `${this.scrollHeight}px`
}

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

async function handleCreateTweet(event) {
  event.preventDefault()
  const form = event.target
  const request = await fetch("/tweets", {
    method: "POST",
    body: new FormData(form),
  })

  const { tweet_id: id, tweet_image_file_name: image_file_name, tweet_text: text } = await request.json()

  if (!request.ok) return alert("Could not tweet")

  const buttonAddImage = formCreateTweet.querySelector("[data-action=add-image]")
  buttonAddImage.addEventListener("click", () => inputAddImage.click())

  const inputAddImage = formCreateTweet.querySelector("[data-hook=input-tweet-image")
  inputAddImage.addEventListener("change", handleTweetAddImage)

  const buttonRemoveImage = formCreateTweet.querySelector("[data-action=remove-image]")
  buttonRemoveImage.addEventListener("click", handleTweetRemoveImage)
  const tweetImageContainer = formCreateTweet.querySelector("[data-hook=tweet-image-container]")
  const tweetImage = formCreateTweet.querySelector("[data-hook=tweet-image]")

  tweetImageContainer.classList.add("is-hidden")
  tweetImage.src = ""
  form.reset()

  const template = templateTweetItem.content.cloneNode(true)
  const dropdown = template.querySelector("[data-dropdown=more]")
  template.querySelector("[data-form=tweet]").setAttribute("data-id", id)
  template.querySelector("[data-field=text]").textContent = text

  if (image_file_name) {
    template.querySelector("[data-field=image]").src = `static/tweets/${image_file_name}`
    template.querySelector("[data-field=image]").classList.remove("is-hidden")
  } else {
    template.querySelector("[data-field=image]").remove()
  }

  template.querySelector("[data-action=delete]").addEventListener("click", handleDeleteTweet)
  template.querySelector("[data-action=edit]").addEventListener("click", handleEditTweet)
  template.querySelector("[data-action=more").addEventListener("click", handleShowMore)
  hookTweets.prepend(template)

  function handleShowMore(event) {
    event.stopPropagation()
    closeOpenDropdown()
    dropdown.classList.remove("hidden")
    document.addEventListener("click", handleHideShowMore)
  }

  function handleHideShowMore(event) {
    if (dropdown.contains(event.target)) closeOpenDropdown()
    dropdown.classList.add("hidden")
    document.removeEventListener("click", handleHideShowMore)
  }

  function closeOpenDropdown() {
    const dropdowns = document.querySelectorAll("[data-dropdown=more]")
    dropdowns.forEach((dropdown) => dropdown.classList.add("hidden"))
  }

  function handleDeleteTweet() {
    modalDeleteTweet.classList.remove("is-hidden")
    modalDeleteTweet.querySelector("[data-action=delete-tweet]").addEventListener("click", requestDeleteTweet)
    modalDeleteTweet.querySelector("[data-action=cancel").addEventListener("click", closeDeleteTweetModal)
    modalDeleteTweet
      .querySelector("[data-target=delete-tweet][data-action=toggle]")
      .addEventListener("click", closeDeleteTweetModal)
  }

  async function requestDeleteTweet() {
    const request = await fetch(`/tweets/${id}`, {
      method: "DELETE",
    })

    const response = await request

    if (!response.ok) return alert("Could not delete tweet")

    hookTweets.querySelector(`[data-form="tweet"][data-id="${id}"]`).remove()
    modalDeleteTweet.classList.add("is-hidden")
  }

  function closeDeleteTweetModal() {
    modalDeleteTweet.querySelector("[data-action=delete-tweet]").removeEventListener("click", requestDeleteTweet)
    modalDeleteTweet.querySelector("[data-action=cancel").removeEventListener("click", closeDeleteTweetModal)
    modalDeleteTweet
      .querySelector("[data-target=delete-tweet][data-action=toggle]")
      .removeEventListener("click", closeDeleteTweetModal)
    modalDeleteTweet.classList.add("is-hidden")
  }

  function handleEditTweet() {
    console.log("edit")
  }
}

const myModal = new Modal(modalDeleteTweet, document.querySelector("[data-action=show-emojis]"))
console.log(myModal)
myModal.openModal()
setTimeout(() => {
  myModal.closeModal()
}, 2000)
