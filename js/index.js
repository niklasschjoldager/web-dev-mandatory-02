const formUserLogin = document.querySelector("[data-form=user-login]")
const formUserSignup = document.querySelector("[data-form=user-signup]")

formUserLogin.addEventListener("submit", handleLogin)
formUserSignup.addEventListener("submit", handleCreateAccount)

async function handleLogin(event) {
  event.preventDefault()

  const request = await fetch("/login", {
    method: "POST",
    body: new FormData(formUserLogin),
  })

  const response = await request

  if (!response.ok) console.log(await response.json())
  if (response.redirected) window.location.href = response.url
}

async function handleCreateAccount(event) {
  event.preventDefault()

  const request = await fetch("/users", {
    method: "POST",
    body: new FormData(formUserSignup),
  })

  const response = await request

  console.log(response)
  if (!response.ok) console.log(await response.json())
}
