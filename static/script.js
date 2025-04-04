document.addEventListener("DOMContentLoaded", function () {
    const sendButton = document.getElementById("send-btn");
    const inputField = document.getElementById("input");
    const chatBox = document.getElementById("chat-box");
    const fileInput = document.getElementById("file-input");
    const filePreview = document.getElementById("file-preview");
  
    // Biến lưu trữ file được tải lên
    let uploadedFile = null;
  
    // Hỗ trợ nhấn Enter để gửi và Shift+Enter để xuống dòng
    inputField.addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        if (event.shiftKey) {
          event.preventDefault();
          inputField.value += "\n";
        } else {
          event.preventDefault();
          sendButton.click();
        }
      }
    });
  
    // Sự kiện khi chọn file: lưu file và hiển thị preview
    fileInput.addEventListener("change", function (event) {
      const file = event.target.files[0];
      if (file) {
        uploadedFile = file;
        // Hiển thị file preview với tên file và nút xóa
        filePreview.innerHTML = `<span>Đã chọn file: ${file.name}</span> <button id="remove-file-btn">Xóa</button>`;
        filePreview.style.display = "flex";
        // Xử lý nút xóa
        document.getElementById("remove-file-btn").addEventListener("click", function () {
          uploadedFile = null;
          filePreview.innerHTML = "";
          filePreview.style.display = "none";
          inputField.placeholder = "Nhập tin nhắn...";
        });
        // Cập nhật placeholder để yêu cầu nhập chú thích (nếu cần)
        inputField.placeholder = ``;
      }
      fileInput.value = ""; // Reset file input
    });
  
    // Sự kiện khi nhấn nút gửi
    sendButton.addEventListener("click", async function () {
      // Nếu có file được tải lên, ưu tiên gửi file kèm chú thích
      if (uploadedFile) {
        const annotation = inputField.value.trim(); // Chú thích nhập vào
        // Hiển thị tin nhắn file với chú thích (nếu có)
        let displayText = `<div class="file-info"><strong>File:</strong> ${uploadedFile.name}</div>`;
        displayText += annotation
          ? `<div class="file-annotation"><em></em> ${annotation}</div>`
          : `<div class="file-annotation"><em></em></div>`;
        appendMessage("user-file", displayText);
        
        // Đọc nội dung file và gửi cho AI
        const fileContent = await readFileContent(uploadedFile);
        
        // Reset file preview và placeholder
        uploadedFile = null;
        filePreview.innerHTML = "";
        filePreview.style.display = "none";
        inputField.value = "";
        inputField.placeholder = "Nhập tin nhắn...";
        
        sendMessageToAI(fileContent);
      } else {
        // Nếu không có file, gửi nội dung văn bản nhập vào
        const userText = inputField.value.trim();
        if (!userText) return;
        appendMessage("user", `👤 Bạn: ${userText}`);
        inputField.value = "";
        sendMessageToAI(userText);
      }
    });
  
    // Hàm đọc nội dung file trả về Promise
    function readFileContent(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = function (e) {
          resolve(e.target.result);
        };
        reader.onerror = function (e) {
          reject(e);
        };
        reader.readAsText(file);
      });
    }
  
    // Hàm gửi tin nhắn đến API
    async function sendMessageToAI(text) {
      const loadingMsg = appendMessage("ai", "🤖 AI đang trả lời...");
      try {
        const response = await fetch("/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: text })
        });
        const data = await response.json();
        removeMessage(loadingMsg);
        if (data.response) {
          const formattedText = formatText(data.response);
          appendMessage("ai", `🤖 AI: ${formattedText}`);
        } else {
          appendMessage("error", "⚠️ Lỗi: AI không có phản hồi.");
        }
      } catch (error) {
        removeMessage(loadingMsg);
        console.error("Error:", error);
        appendMessage("error", "⚠️ Lỗi kết nối API. Vui lòng thử lại.");
      }
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  
    // Hàm hiển thị tin nhắn
    function appendMessage(type, text) {
      const msgDiv = document.createElement("div");
      if (type === "user") {
        msgDiv.className = "user-msg";
      } else if (type === "user-file") {
        msgDiv.className = "user-file-msg";
      } else if (type === "ai") {
        msgDiv.className = "ai-msg";
      } else if (type === "error") {
        msgDiv.className = "error-msg";
      }
      msgDiv.innerHTML = text;
      chatBox.appendChild(msgDiv);
      chatBox.scrollTop = chatBox.scrollHeight;
      return msgDiv;
    }
  
    // Hàm xóa tin nhắn (dùng cho loading)
    function removeMessage(element) {
      if (chatBox.contains(element)) {
        chatBox.removeChild(element);
      }
    }
  
    // Hàm định dạng văn bản: loại bỏ dấu ** và chuyển \n thành <br>
    function formatText(text) {
      return text.replace(/\*\*(.*?)\*\*/g, "$1").replace(/\n/g, "<br>");
    }
  });
  