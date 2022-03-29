export default class Modal {
  constructor(modal, target) {
    this.modal = modal
    this.target = target
    this.openClass = "is-hidden"
    this.onOpen = () => console.log("Do stuff when I open")
    this.onClose = () => console.log("Do stuff after I close")
    this.openModal = this.openModal.bind(this)
    this.closeModal = this.closeModal.bind(this)
    this.target.addEventListener("click", this.openModal)
  }

  openModal() {
    console.log(this.openClass)
    this.modal.classList.remove(this.openClass)
    this.onOpen()
    this.addListeners()
  }

  closeModal() {
    this.modal.classList.add(this.openClass)
    this.onClose()
    this.removeListeners()
  }

  addListeners() {
    this.target.addEventListener("click", this.closeModal)
    this.modal.querySelector("[data-modal-backdrop]").addEventListener("click", this.closeModal)
    this.modal.querySelector("[data-modal-dismiss").addEventListener("click", this.closeModal)
  }

  removeListeners() {
    this.target.removeEventListener("click", this.closeModal)
    this.modal.querySelector("[data-modal-backdrop]").removeEventListener("click", this.closeModal)
    this.modal.querySelector("[data-modal-dismiss").removeEventListener("click", this.closeModal)
  }
}
