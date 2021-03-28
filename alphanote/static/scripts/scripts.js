const navDropdown = document.querySelector("#single-dropdown");
const modalTriggers = document.querySelectorAll(".account-trigger");
const accountModal = document.querySelector("#account-modal");
const optionContainer = document.querySelector('#option-container');
const navWrapper = document.querySelector(".nav-main");
const bodyRect = document.body.getBoundingClientRect()
const actionButton = document.querySelector(".fixed-action-btn");
const updateNoteForm = document.querySelector(".update-note");
const noteDeletBtn = document.getElementsByClassName("deleteNote");
const mainWrapper = document.querySelector('.wrapper-main');
const summerNoteConfig = {
  'toolbar': [
    ['style', ['style']],
    ['font', ['bold', 'underline', 'clear']],
    ['fontname', ['fontname']],
    ['color', ['color']],
    ['para', ['ul', 'ol', 'paragraph']],
    ['table', ['table']],
    ['view', ['codeview', 'help']],
  ]
}

/* get page cookie */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/* get csrf token from cookie */
const csrftoken = getCookie('csrftoken');

/* set multiple css sttributes */
function setAttributes(el, attrs) {
  for(var key in attrs) {
    el.setAttribute(key, attrs[key]);
  }
  return el;
}

/* get coordinates of elem */
function getCoords(elem) {
  let box = elem.getBoundingClientRect();

  return {
    top: box.top + window.pageYOffset,
    right: box.right + window.pageXOffset,
    bottom: box.bottom + window.pageYOffset,
    left: box.left + window.pageXOffset
  };
}

/* create object out of card-element to keep info */
class Card {
  
  /**
  * @param {Element} element - The card body element
  */
 
 constructor (element) {
   this.cardElement = element;
   this.dimensions = element.getBoundingClientRect()
   this.cardTitle = element.querySelector('.card-subject');
   this.cardContent = element.querySelector('.card-content');
   this.cardExtra = element.querySelector('.card-extras');
   this.cardSrc = element.getAttribute('data-src');
  }
}

/** main wrapper object 
* wide tracking instead of card tracking, challenge
*/
class Mainwrapper {

  /**
  * @param {Element} element - Main wrapper element
  */
  constructor(element) {
    this.element = element;
    this.element.addEventListener("click", this.delegateCardClicked.bind(this));
  }

  /**
  * @param {Event} event - Event obj from listener
  */
  delegateCardClicked (event) {
    
    let eventTarget = event.target;
    let cardClicked = event.target.closest('.card-main');
    if (cardClicked !== null && !(eventTarget instanceof HTMLAnchorElement)) {this.handleCardClicked(event, eventTarget, cardClicked)}
    else if (optionHandler) {
      if (optionHandler.isOpen === true) optionHandler.closeOption();
    }
  }

  /* called if clicked area has card main as ancestor */
  handleCardClicked (event, eventTarget, cardElement) {
    let cardObj = new Card(cardElement)
    let eventAction = eventTarget.getAttribute('data-bs') ? eventTarget.getAttribute('data-bs') : cardElement.getAttribute('data-bs');

    switch (eventAction) {
      
      case 'delNotebook':
      case 'delNote': {
        let delUrl = eventTarget.closest('button').getAttribute('href');
        optionHandler.setOption('delete', cardObj, delUrl);
        optionHandler.showOption(cardObj);
        break;
      }
      
      case 'delCancel':
        optionHandler.closeOption()
        break;
      
      case 'delConfirm':
        let delBtn = eventTarget.closest('button');
        optionHandler.performDelete(cardObj, delBtn)
        break;
      
      case 'opt-trigger':
        optionHandler.setOption('notebook', cardObj);
        optionHandler.showOption(cardObj);
        break;
      
      case 'opt-close':
        optionHandler.closeOption()
        break;
      
      case 'noteUpdate':
        let form = eventTarget.closest('.opt-content').querySelector('form');
        optionHandler.updateNotebook(cardObj, form)
        break;
      
      case 'noteCancel':
        optionHandler.closeOption()
        break;

      case 'noteCard':
        if (optionHandler.isOpen === true && optionHandler.onCardObj === cardObj.cardSrc) break;
        else myModal.buildModal('card', cardObj)
        break;

      default:
        break;
    }
  }
}

/* class for option modal */
class OptionHandler {
  /**
  * @param {Element} divContainer - The option container
  */

  constructor(divContainer) {
    this.optionContainer = divContainer;
    this.optionBody = this.optionContainer.querySelector('.opt-body');
    this.optionFooter = this.optionContainer.querySelector('.opt-footer');
    this.optionContents = {}
    this.isOpen = false;
    this.onCardObj = null;
    this.optionType = null;
  }


  /**open option menu 
  * @param {Card} cardObj - The card object
  */
  showOption (cardObj) {
    cardObj.cardElement.prepend(this.optionContainer);
    this.optionContainer.style.cssText += ';' + `display: grid; position: absolute;
    height: 100%; width: 100%; z-index: 3;`
    this.isOpen = true;
    this.onCardObj = cardObj.cardSrc;
  }

  /* close option menu */
  closeOption () {
    this.optionContainer.style.cssText = '';
    this.clearOption()
    this.isOpen = false;
    this.onCardObj = null;
    this.optionType = null;
    accountModal.insertAdjacentElement('afterend', this.optionContainer);
  }

  /* clears option */
  clearOption () {
    this.optionBody.innerHTML ='';
    this.optionFooter.innerHTML = '';
  }

  /* fills option menu */
  setOption (arg, cardObj, url) {
  
    switch (arg) {

      case 'delete': {
        if (this.isOpen &&  this.onCardObj === cardObj.cardSrc && this.optionType === 'delete') break;
        this.clearOption();
        this.createDeleteOption(url);
        this.optionType = 'delete';
        break;
      }
      case 'notebook': {
        if (this.isOpen &&  this.onCardObj === cardObj.cardSrc && this.optionType === 'notebook') break;
        this.clearOption()
        this.createNotebookOption(cardObj);
        this.optionType = 'notebook';
        break;
      }
    }
  }

  /* creates delete form */
  createDeleteOption (url) {
    this.optionBody.innerHTML = '<p>Delete this Note?</p>';
    const button = `<button type="button" class="btn bttn--choice__yes" data-bs="delConfirm" data-target="${url}"><span>Yes</span>
                    <div class="icon" data-bs="delConfirm">
                      <i class="initial bi bi-check-square" data-bs="delConfirm"></i>
                      <i class="after bi bi-check-square-fill" data-bs="delConfirm"></i>
                    </div>
                    </button>
                    <button type="button" class="btn bttn--choice__no" data-bs="delCancel" data-target="${url}"><span>No</span>
                    <div class="icon" data-bs="delCancel">
                      <i class="initial bi bi-x-circle" data-bs="delCancel"></i>
                      <i class="after bi bi-x-circle-fill" data-bs="delCancel"></i>
                    </div>
                    </button>`
    this.optionFooter.innerHTML = button;
  }

  /* create/get notebook form */
  async createNotebookOption (cardObj) {
    let form = await resourcer.newRequest('GET', `${document.location.origin}/notes/update/${cardObj.cardSrc}/`)
    const button = `<button type="button" class="btn bttn--choice__yes" data-bs="noteUpdate"><span>Update</span>
                    <div class="icon" data-bs="noteUpdate">
                      <i class="initial bi bi-check-square" data-bs="noteUpdate"></i>
                      <i class="after bi bi-check-square-fill" data-bs="noteUpdate"></i>
                    </div>
                    </button>
                    <button type="button" class="btn bttn--choice__no" data-bs="noteCancel"><span>Cancel</span>
                    <div class="icon" data-bs="noteCancel">
                      <i class="initial bi bi-x-circle" data-bs="noteCancel"></i>
                      <i class="after bi bi-x-circle-fill" data-bs="noteCancel"></i>
                    </div>
                    </button>`
    this.optionBody.innerHTML = form.ok? form.response : '<div> Error fetching notebooks </div>'
    this.optionFooter.innerHTML = button;
  }

  async performDelete (cardObj, btnElement) {
    let href = btnElement.getAttribute('data-target');
    let mUrl = `${document.location.origin}${href}`
    let response = await resourcer.newRequest('POST', mUrl);
    if (response.ok) {
      btnElement.classList.add('success')
      animator.animate(cardObj.cardElement, 'DELETE')
      utils.removeSuccessClass(btnElement)
      return utils.callToast('Item Deleted');
    } 
    utils.callToast('Error while deleting item', 5000)
    optionHandler.closeOption()
  }  

  /* handles when update confirmed */
  async updateNotebook (cardObj, formElem) {
    let options = {}
    options['formData'] = resourcer.generateFormdata(formElem);
    options['name'] = 'updateNotebook';
    let response = await resourcer.newRequest('POST', `${document.location.origin}/notes/update/${cardObj.cardSrc}/`, options);
    if (response.ok) {
      this.closeOption()
      return utils.callToast('Notebook Updated');
    }
    utils.callToast('Update Failed', 5000)
    optionHandler.closeOption()
  }

}

/* class for resource handling, fetching or posting */
class ResourceHandler {
  
  constructor () {
    this.responseObj = null;
    this.responseString = null;
    this.formObj = null;
  }

  /**
  * @param {string} methodType - The operation method post or get
  * @param {string} url - The operation url
  * @param {Object} options - options to add/change behaviour
  */

  async newRequest (methodType, url, options=false) {
    this.method = methodType;
    this.url = url;
    this.requestOptions = {method: this.method, mode: 'same-origin'}
    this.options = options

    if (this.method === 'POST') this.requestOptions['headers'] = {'X-CSRFToken': csrftoken};
    if (options) {
      if (options.name === 'updateNotebook') {this.requestOptions['body'] = options.formData}
    }
    
    let request = new Request(this.url, this.requestOptions);
    try {
      this.responseObj = await fetch(request)
    } catch (error) {
      this.responseObj = {'ok' : false, 'error': 'Resource Unreachable'}
      return this.responseObj
    }
    this.responseString = await this.responseObj.text()
    if (this.method === 'POST') return this.responseObj;
    return {ok: true, response: this.responseString };
  }

  /**generate form data
  *  @param {Element} element - element to generate form from
  */
  generateFormdata (element) {
    this.formObj = new FormData(element);
    return this.formObj;
  }
}

/* class for my custom modal*/
class ModalHandler {
  /**
  *  @param {Element} modalElement - the modal container
  *  @param {Element} modalTriggers - html element that triggers modal
  */

  constructor(modalElement, modalTriggers) {
    this.modalContainer = modalElement;
    this.modalTriggers = modalTriggers;
    this.modalHeader = this.modalContainer.querySelector(".modal-header");
    this.modalBody = this.modalContainer.querySelector(".modal-body");
    this.modalFooter = this.modalContainer.querySelector(".modal-footer");
    this.triggerClicked = '';
    this.triggerAction = '';
    this.triggerTargetUrl = '';
    this.modalTriggers.forEach( (element) => element.addEventListener('click', this.delegateEvent.bind(this)) )
  }

  delegateEvent (eventObj) {
    this.triggerClicked = eventObj.target;
    this.triggerTargetUrl = this.triggerClicked.getAttribute('data-url');
    this.triggerAction = this.triggerClicked.getAttribute('data-bs');
    this.buildModal(this.triggerAction)
  }

  /** main function for handling modal process
  * 
  */
  async buildModal(triggerAction, cardObj) {

    switch (triggerAction) {

      case 'logout': {
        let modalElements = this.logoutModal()
        this.fillModalElements(modalElements)
        break;
      }
      case 'password-reset':{
        let formElement = await resourcer.newRequest('GET', this.triggerTargetUrl);
        let modalElements = this.passwordResetModal();
        if (formElement.ok) {
          modalElements['body'].push(formElement.response);
          this.fillModalElements(modalElements);
        } else {
          this.fillModalElements({'body': ['Error Fetching Note'], 'footer': ['Please try again']})
        }
        break;
      }
      case 'card': {
        let useModal = this.getMaterializeModal(accountModal);
        useModal.open();
        let formElement = await resourcer.newRequest('GET', `${document.location.origin}/notes/view/${cardObj.cardSrc}/`);
        if (formElement.ok) {
          let modalElements = {'body': [formElement.response], 'footer': ['']}
          this.fillModalElements(modalElements)
          $('#field_content').summernote(summerNoteConfig);
        } else {
          this.fillModalElements({'body': ['Error Fetching Note'], 'footer': ['Please try again']})
        }
        break;
      }
      default:
        break;
    }
  }

  /* creates and shows logout modal */
  logoutModal () {
    let elemCreated = {'header': [], 'body': [], 'footer': []}
    let message = document.createElement('h1');
    let form = document.createElement('form');
    let csrfInput = document.createElement('input')
    message.textContent = "Are you sure you want to sign out?"
    setAttributes(form, {"id": "accountForm", method: 'POST', 'action': `${this.triggerTargetUrl}`})
    setAttributes(csrfInput, {"type": 'hidden', 'name': 'csrfmiddlewaretoken', 'value':`${csrftoken}`})
    form.appendChild(csrfInput)
    const logoutConfirm = document.createElement('button');
    setAttributes(logoutConfirm, {'class': 'bttn--base', 'type': 'submit', 'form': "accountForm"});
    logoutConfirm.innerText = 'Logout'; 
    const logoutCancel = document.createElement('button');
    setAttributes(logoutCancel, {'class': 'bttn--base modal-close', 'type': 'button'})
    logoutCancel.innerText = 'Cancel';
    elemCreated['footer'].push(logoutConfirm);
    elemCreated['footer'].push(logoutCancel);
    elemCreated['header'].push(message);
    elemCreated['body'].push(form)
    return elemCreated;
  }

  /* creates and shows password reset modal */
  passwordResetModal () {
    let elemCreated = {'header': [], 'body': [], 'footer': []}
    let message = document.createElement('h3');
    message.textContent = "Enter your e-mail address below, and we'll send you an e-mail allowing you to reset it"
    const resetConfirm = document.createElement('button');
    setAttributes(resetConfirm, {'class': 'bttn--base', 'type': 'submit'});
    resetConfirm.innerHTML = 'reset password';
    elemCreated['footer'].push(resetConfirm);
    elemCreated['header'].push(message);
    return elemCreated;
  }

  /** Fill out the modal
  * @param {Object} elementObjects - object of keys: header,body,footer and values: html or node
  */
  fillModalElements (elementObjects) {

    for (let [key,value] of Object.entries(elementObjects)) {
      if (value.length === 0) continue;
      for (let element of value) {

        switch (key) {
          
          case 'header':
            if (typeof(element) == 'string') {this.modalHeader.innerHTML = element}
            else {this.modalHeader.appendChild(element)}
            break;
          
          case 'body':
            if (typeof(element) == 'string') {this.modalBody.innerHTML = element}
            else {this.modalBody.appendChild(element)}
            break;
          
          case 'footer':
            if (typeof(element) == 'string') {this.modalFooter.innerHTML = element}
            else {this.modalFooter.appendChild(element)}
            break;
        
          default:
            break;
        }
      }
    }
  }

  /**gets the materialize modal instance
  *  @param {Element} element - modal element
  */ 
  getMaterializeModal (element) {
    let modalInstance = M.Modal.getInstance(element)
    return modalInstance
  }

  /* called from materialize.js */
  clearModalContent () {
    this.modalHeader.innerHTML = ""
    this.modalBody.innerHTML = ""
    this.modalFooter.innerHTML = ""
  }
}

/* random utility */
class Utility {

  constructor () {
    this.activeElement = null;
  }

  /* method for active class */
  activeMarker () {
    let allNavItems = Array.from(navWrapper.children);
    allNavItems.forEach( function (item) {
      if (item.getAttribute('href') === document.location.pathname) {
        item.classList.add('active')
        this.activeElement = item;
      }
    }.bind(this))
  }

  callToast (message, length=null) {
    let options = {
      'html': message,
      'classes': 'rounded'
    }
    options['displayLength'] = length ? length : 2000
    M.toast(options);
  }

  removeSuccessClass (btnElement) {
    setTimeout( function () {
      btnElement.classList.remove('success')
    }, 3000)
  }
}

class AnimationHandler {

  /**
  * @param {Function} anime - The anime function from anime.min.js
  */
  constructor (anime) {
    this.animeobj = anime;
    this.deleteAnimation = {targets: 'ELEM',
                              translateY: [
                                {value: 30, duration: 200, easing: 'easeOutCubic'},
                                {value: 0, duration: 300, delay: 200, easing: 'easeOutCubic'}
                              ],
                              scale: [
                                {value: 0, duration: 300, delay: 500, easing: 'linear'}
                              ]
                            }
  }

  /**
  * @param {Element} elem - The Element to be animated
  * @param {String} type - Animation Type
  */
  async animate (elem, type) {

    // select animation to be applied
    switch (type) {
      case 'DELETE':
        this.deleteAnimation['targets'] = elem;
        break;
    
      default:
        break;
    }

    // start and await animation
    let animationResult = anime(this.deleteAnimation);
    await animationResult.finished
    elem.remove()

    // always return a promise, catch errors
    return animationResult;

  }
}

/* materialize initializers */
$('.dropdown-trigger').dropdown();
document.addEventListener('DOMContentLoaded', function() {
  var modalElems = document.querySelectorAll('.modal');
  var stickyElems = document.querySelectorAll('.fixed-action-btn');
  var modalOptions = {'dismissible': true, 'startingTop':'2%', 'endingTop': '6%'}
  var stickyOptions = {'direction': 'top', 'hoverEnabled': false}
  var modalInstances = M.Modal.init(modalElems, modalOptions);
  var stickyInstances = M.FloatingActionButton.init(stickyElems, stickyOptions);
}); 

const callToast = function(message) {
  let options = {
    'html': message,
    'displayLength': 2000,
    'classes': 'rounded'
  }
  M.toast(options);
}

const optionHandler = optionContainer ? new OptionHandler(optionContainer) : null;
const wrapper = new Mainwrapper(mainWrapper)
const resourcer = new ResourceHandler()
const myModal = new ModalHandler(accountModal, modalTriggers)
const utils = new Utility()
const animator = new AnimationHandler(anime)
utils.activeMarker()
