var scroller = document.querySelector("#scroller");
var loaded = document.querySelector("#loaded");
var sentinel = document.querySelector('#sentinel');

// Set a counter to count the items loaded
var counter = 0;
// Function to request new items and render to the dom
function loadItems() {

  // Use fetch to request data and pass the count value in the QS
  fetch(`/load?c=${sentinel.getAttribute("data-count")}`).then((response) => {

    // Convert the response data to JSON
    response.json().then((data) => {

      // If empty JSON, exit the function
      if (!data.length) {
                  // Replace the spinner with "No more posts"
  sentinel.innerHTML = "No more posts";
  return;
}

// Iterate over the items in the response
for (var i = 0; i < data.length; i++) {
    if (i % 2 === 0) {
        var template = document.querySelector('#post_template_1');
    } else {
        var template = document.querySelector('#post_template_2');
    }
    let template_clone = template.content.cloneNode(true);
    template_clone.querySelector("#title").innerHTML = `${data[i]['title']}`;
    template_clone.querySelector("#content").innerHTML = data[i]['content'];  
    scroller.appendChild(template_clone);

}

// Increment the count on the sentinel element
sentinel.setAttribute("data-count", parseInt(sentinel.getAttribute("data-count")) + 1);

// Update the counter in the navbar
loaded.innerText = `${parseInt(sentinel.getAttribute("data-count")) * 9} posts loaded`;

})
})
}

// Create a new IntersectionObserver instance
var intersectionObserver = new IntersectionObserver(entries => {

// If intersectionRatio is 0, the sentinel is out of view
// and we don't need to do anything. Exit the function
if (entries[0].intersectionRatio <= 0) {
return;
}

// Call the loadItems function
loadItems();

});

// Instruct the IntersectionObserver to watch the sentinel
intersectionObserver.observe(sentinel);

