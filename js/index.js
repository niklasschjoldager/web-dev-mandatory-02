const formUserLogin = document.querySelector("[data-form=user-login]")

formUserLogin.addEventListener("submit", login)

async function login(event) {
  event.preventDefault()

  const request = await fetch("/login", {
    method: "POST",
    body: new FormData(formUserLogin),
  })

  const response = await request

  if (!response.ok) console.log(await response.json())
  if (response.redirected) window.location.href = response.url
}
