(function() {
    // This script would be injected into the ChatGPT page

    // Function to handle the click event on the microphone button
    function handleMicrophoneClick(event) {
      event.preventDefault();
      event.stopPropagation();

      // Get the content of the textarea
      const text = document.querySelector('#prompt-textarea').value;

      // Send a message to the background script with the content of the textarea
      chrome.runtime.sendMessage({ command: "start_recording", text: text });

      console.log('Microphone button clicked. Message sent to background script:', { command: "start_recording", text: text });
    }

    // Try to find the parent element of the chat input area by navigating up from the textarea
    const chatTextarea = document.querySelector('#prompt-textarea');
    if (!chatTextarea) {
      console.error('Chat textarea not found.');
      return;
    }

    // Assume the grandparent of the textarea is the container controlling the width
    const chatInputContainer = chatTextarea.parentElement.parentElement;
    if (!chatInputContainer) {
      console.error('Chat input container not found.');
      return;
    }

    // Adjust the width of the chat input container to create space for the microphone button
    chatInputContainer.style.width = 'calc(100% - 60px)';  // Adjust the width as needed

    // Create a microphone button
    const microphoneButton = document.createElement('button');
    microphoneButton.innerText = '🎤';  // Microphone emoji as button text
    microphoneButton.style.position = 'absolute';
    microphoneButton.style.right = '20px';  // Position to the right of the chat box, adjust as needed
    microphoneButton.style.top = '50%';  // Center vertically in relation to the chat box
    microphoneButton.style.transform = 'translateY(-50%)';  // Adjust vertical positioning
    microphoneButton.style.zIndex = '1000';  // Ensure it's above other elements
    microphoneButton.style.backgroundColor = 'transparent';  // Transparent background
    microphoneButton.style.border = 'none';  // No border
    microphoneButton.style.cursor = 'pointer';  // Cursor pointer on hover
    microphoneButton.style.fontSize = '24px';  // Adjust the size as needed
    microphoneButton.addEventListener('click', handleMicrophoneClick);

    // Append the microphone button as a sibling to the chat input container
    chatInputContainer.parentNode.insertBefore(microphoneButton, chatInputContainer.nextSibling);
    console.log('Microphone button added.');
})();
