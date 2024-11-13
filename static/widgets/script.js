const getColor = (color, shade) => {
  if (color === "green") {
    if (shade === "50") {
      return "#f0fdf4";
    } else if (shade === "100") {
      return "#dcfce7";
    } else if (shade === "200") {
      return "#bbf7d0";
    } else if (shade === "300") {
      return "#86efac";
    } else if (shade === "400") {
      return "#4ade80";
    } else if (shade === "500") {
      return "#22c55e";
    } else if (shade === "600") {
      return "#16a34a";
    } else if (shade === "700") {
      return "#15803d";
    } else if (shade === "800") {
      return "#166534";
    } else if (shade === "900") {
      return "#14532d";
    }
  } else if (color === "blue") {
    if (shade === "50") {
      return "#eff6ff";
    } else if (shade === "100") {
      return "#dbeafe";
    } else if (shade === "200") {
      return "#bfdbfe";
    } else if (shade === "300") {
      return "#93c5fd";
    } else if (shade === "400") {
      return "#60a5fa";
    } else if (shade === "500") {
      return "#3b82f6";
    } else if (shade === "600") {
      return "#2563eb";
    } else if (shade === "700") {
      return "#1d4ed8";
    } else if (shade === "800") {
      return "#1e40af";
    } else if (shade === "900") {
      return "#1e3a8a";
    }
  } else if (color === "red") {
    if (shade === "50") {
      return "#fef2f2";
    } else if (shade === "100") {
      return "#fee2e2";
    } else if (shade === "200") {
      return "#fecaca";
    } else if (shade === "300") {
      return "#fca5a5";
    } else if (shade === "400") {
      return "#f87171";
    } else if (shade === "500") {
      return "#ef4444";
    } else if (shade === "600") {
      return "#dc2626";
    } else if (shade === "700") {
      return "#b91c1c";
    } else if (shade === "800") {
      return "#991b1b";
    } else if (shade === "900") {
      return "#7f1d1d";
    }
  } else if (color === "white" || color === "black") {
    if (shade === "50") {
      return "#ffffff";
    } else if (shade === "100") {
      return "#f3f4f6";
    } else if (shade === "200") {
      return "#e5e7eb";
    } else if (shade === "300") {
      return "#d1d5db";
    } else if (shade === "400") {
      return "#9ca3af";
    } else if (shade === "500") {
      return "#6b7280";
    } else if (shade === "600") {
      return "#52525b";
    } else if (shade === "700") {
      return "#3f3f46";
    } else if (shade === "800") {
      return "#1f2937";
    } else if (shade === "900") {
      return "#000000";
    }
  }
};

const chatbot_id = document.currentScript.getAttribute("chatbot_id") || "34";

const user_id = document.currentScript.getAttribute("user_id") || "83";

if (chatbot_id === "") {
  console.error("Chatbot ID is required");
}

const bubbleBoxShadow =
  document.currentScript.getAttribute("bubbleBoxShadow") || "outer";

const bubbleBorder =
  document.currentScript.getAttribute("bubbleBorder") || "false";

const bubbleAlignment =
  document.currentScript.getAttribute("bubbleAlignment") || "horizontal";

const isVoiceChatActive = document.currentScript.getAttribute("voice") || false;

const isFeedbackActive =
  document.currentScript.getAttribute("feedback") || false;

const headerColor =
  document.currentScript.getAttribute("headerColor") || "white";
const headerColorShade =
  document.currentScript.getAttribute("headerColorShade") || "100";
const buddleColor =
  document.currentScript.getAttribute("buddleColor") || "white";
const buddleColorShade =
  document.currentScript.getAttribute("buddleColorShade") || "100";
const textColor = document.currentScript.getAttribute("textColor") || "black";

const textColorShade =
  document.currentScript.getAttribute("textColorShade") || "700";

const voiceIndicator = isVoiceChatActive
  ? `<div
            style="
              border-radius: 9999px;
              width: 40px;
              height: 40px;
              color: #fff;
              background-color: #dc2626;
              padding: 0.5rem;
            "
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              aria-hidden="true"
              data-slot="icon"
              class="h-6 w-6 text-gray-200"
            >
              <path
                d="M8.25 4.5a3.75 3.75 0 1 1 7.5 0v8.25a3.75 3.75 0 1 1-7.5 0V4.5Z"
              ></path>
              <path
                d="M6 10.5a.75.75 0 0 1 .75.75v1.5a5.25 5.25 0 1 0 10.5 0v-1.5a.75.75 0 0 1 1.5 0v1.5a6.751 6.751 0 0 1-6 6.709v2.291h3a.75.75 0 0 1 0 1.5h-7.5a.75.75 0 0 1 0-1.5h3v-2.291a6.751 6.751 0 0 1-6-6.709v-1.5A.75.75 0 0 1 6 10.5Z"
              ></path>
            </svg>
          </div>`
  : `<span></span>`;

const feedbackButtons = isFeedbackActive
  ? `<div class="mt-3 flex gap-1">
   <svg class="h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
      <path fill="currentColor" fill-rule="evenodd" d="M7 5a3 3 0 0 1 3-3h9a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-2v2a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3h2zm2 2h5a3 3 0 0 1 3 3v5h2a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1h-9a1 1 0 0 0-1 1zM5 9a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h9a1 1 0 0 0 1-1v-9a1 1 0 0 0-1-1z" clip-rule="evenodd"></path>
   </svg>
   <svg class="h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
      <path fill="currentColor" fill-rule="evenodd" d="M11.873 21.496a1 1 0 0 1-.992.496l-.454-.056A4 4 0 0 1 7.1 16.79L7.65 15h-.718c-2.637 0-4.553-2.508-3.859-5.052l1.364-5A4 4 0 0 1 8.296 2h9.709a3 3 0 0 1 3 3v7a3 3 0 0 1-3 3h-2c-.26 0-.5.14-.628.364zM14.005 4h-5.71a2 2 0 0 0-1.929 1.474l-1.363 5A2 2 0 0 0 6.933 13h2.072a1 1 0 0 1 .955 1.294l-.949 3.084a2 2 0 0 0 1.462 2.537l3.167-5.543a2.72 2.72 0 0 1 1.364-1.182V5a1 1 0 0 0-1-1m3 9V5c0-.35-.06-.687-.171-1h1.17a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1z" clip-rule="evenodd"></path>
   </svg>
</div>`
  : "";

document.body.innerHTML += `<div>
    <!-- <div class="loader"></div> -->
    <button style="z-index: 50" class="chatbot-toggler">
      <svg
        style="padding: 4px"
        width="40px"
        height="40px"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M8 12H8.01M12 12H12.01M16 12H16.01M21.0039 12C21.0039 16.9706 16.9745 21 12.0039 21C9.9675 21 3.00463 21 3.00463 21C3.00463 21 4.56382 17.2561 3.93982 16.0008C3.34076 14.7956 3.00391 13.4372 3.00391 12C3.00391 7.02944 7.03334 3 12.0039 3C16.9745 3 21.0039 7.02944 21.0039 12Z"
          stroke="#fff"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        ></path>
      </svg>
      <svg
        width="30px"
        height="30px"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M20.7457 3.32851C20.3552 2.93798 19.722 2.93798 19.3315 3.32851L12.0371 10.6229L4.74275 3.32851C4.35223 2.93798 3.71906 2.93798 3.32854 3.32851C2.93801 3.71903 2.93801 4.3522 3.32854 4.74272L10.6229 12.0371L3.32856 19.3314C2.93803 19.722 2.93803 20.3551 3.32856 20.7457C3.71908 21.1362 4.35225 21.1362 4.74277 20.7457L12.0371 13.4513L19.3315 20.7457C19.722 21.1362 20.3552 21.1362 20.7457 20.7457C21.1362 20.3551 21.1362 19.722 20.7457 19.3315L13.4513 12.0371L20.7457 4.74272C21.1362 4.3522 21.1362 3.71903 20.7457 3.32851Z"
          fill="#fff"
        />
      </svg>
    </button>
    <div class="chatbot">
      <header style="background: ${getColor(headerColor, headerColorShade)};">
        <h2>Chat</h2>
        <button
          style="
            background: none;
            border: none;
            cursor: pointer;
            font-size: large;
          "
        >
          <svg
            width="15"
            height="15"
            viewBox="0 0 15 15"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            class="h-4 w-4"
          >
            <path
              d="M12.8536 2.85355C13.0488 2.65829 13.0488 2.34171 12.8536 2.14645C12.6583 1.95118 12.3417 1.95118 12.1464 2.14645L7.5 6.79289L2.85355 2.14645C2.65829 1.95118 2.34171 1.95118 2.14645 2.14645C1.95118 2.34171 1.95118 2.65829 2.14645 2.85355L6.79289 7.5L2.14645 12.1464C1.95118 12.3417 1.95118 12.6583 2.14645 12.8536C2.34171 13.0488 2.65829 13.0488 2.85355 12.8536L7.5 8.20711L12.1464 12.8536C12.3417 13.0488 12.6583 13.0488 12.8536 12.8536C13.0488 12.6583 13.0488 12.3417 12.8536 12.1464L8.20711 7.5L12.8536 2.85355Z"
              fill="currentColor"
              fill-rule="evenodd"
              clip-rule="evenodd"
            ></path>
          </svg>
        </button>
      </header>
      <hr
        style="
          border-top-width: 1px;
          border-top-style: solid;
          border-top-color: hsl(214.3 31.8% 91.4%);
        "
      />
      <div
        class="chatbox"
        style="
          position: relative;
          padding-bottom: 10px;
          display: flex;
          flex-direction: column;
          justify-content: flex-end;
          align-items: flex-start;
        "
      >
        <div
          id="chatbot__welcome_animation"
          style="
            position: absolute;
            bottom: 0;
            left: 50%;
            width: 85%;
            transform: translate(-50%, 0);
            margin: auto;
          "
        >
          <div id="chatbot__sample_qustion" >
          
            </div>
          
         
        </div>
        <div
          id="chatbot__conversation"
          style="
            width: 100%;
            margin-top: auto;
            max-height: 100%;
            overflow: auto;
            padding: 0 2rem 0 2rem;
          "
        ></div>
      </div>
      <div style="width: 100%">
        <form class="chat-input" action="">
          ${voiceIndicator}
          
          <div
            style="
              flex: 1 1 0%;
              display: flex;
              align-items: center;
              border: 1px solid hsl(214.3 31.8% 91.4%);
              border-radius: 10px;
            "
          >
            <input placeholder="Enter a message..." />
            <svg
              id="send-btn"
              style="
                width: 1.5rem;
                height: auto;
                margin-right: 0.75rem;
                cursor: pointer;
              "
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              aria-hidden="true"
              data-slot="icon"
              class="mr-2 h-5 w-5"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5"
              ></path>
            </svg>
          </div>
        </form>
      </div>
    </div>

    <!-- <div
      id="overlay"
      style="
        height: 100vh;
        width: 100vw;
        background: rgba(0, 0, 0, 0.5);
        z-index: 10;
      "
      class="overlay"
    /> -->
  </div>`;

const style = document.createElement("style");
style.innerHTML = `
.chatbot-toggler {
        position: fixed;
        bottom: 30px;
        right: 35px;
        outline: none;
        border: none;
        height: 50px;
        width: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;

        border-radius: 50%;
        background: #585979;
        transition: all 0.2s ease;
      }

      .show-chatbot .chatbot-toggler {
        transform: rotate(90deg);
      }

      .chatbot-toggler svg {
        position: absolute;
      }

      .show-chatbot .chatbot-toggler svg:first-child,
      .chatbot-toggler svg:last-child {
        opacity: 0;
      }

      .show-chatbot .chatbot-toggler svg:last-child {
        opacity: 1;
      }

      .chatbot {
        font-family: "Inter", sans-serif;
        position: fixed;
        z-index: 999;
        width: 380px;
        right: 35px;
        bottom: 90px;
        transform: scale(0.5);
        opacity: 0;
        pointer-events: none;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        border-radius: 0.5rem;
        border: hsl(214.3 31.8% 91.4%);
        border-width: 1px;
        border-style: solid;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding-bottom: 1.25rem;

      }

      hr {
        border: hsl(214.3 31.8% 91.4%);
      }

      .show-chatbot .chatbot {
        transform: scale(1);
        opacity: 1;
        pointer-events: auto;
      }

      .chatbot header {
        display: flex;
        justify-content: space-between;
        padding-bottom: 1.25rem; /* 5 */
        padding-left: 2rem; /* 8 */
        padding-right: 1.25rem; /* 5 */
        padding-top: 1.25rem; /* 5 */
        background-color: #ffffff; /* white */
        color: rgba(56, 56, 56, 0.9); /* text-gray-900/90 */
      }

      .chatbot header h2 {
        font-size: 1.5rem; /* text-xl */
        font-weight: 700; /* font-bold */
      }

      .chatbot .chatbox {
        height: 440px;
        overflow-y: auto;
        width: 100%;
      }

      .chatbot .chat__bubble {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 0.75rem;
        
      }

      .incoming {
        flex-direction: ${bubbleAlignment === "horizontal" ? "row" : "column"};
        justify-content: flex-start;
      }

      .outgoing {
        flex-direction: ${
          bubbleAlignment === "horizontal" ? "row-reverse" : "column"
        };
        justify-content: flex-end;
      }

      .chatbot .chat__bubble___header {
        // margin-left: 0.5rem;
        // margin-right: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding-top: 0.25rem;
        padding-bottom: 0.25rem;
        justify-content: flex-start;
      }
      .chatbot .chat__bubble___header svg {
        height: 1.5rem;
        width: 1.5rem;
        border-radius: 9999px;
        object-fit: cover;
        color: #3b82f6;
      }

      .chatbot .chat__bubble___header .chatbot__user__name {
        font-size: 0.875rem;
        font-weight: 600;
        color: #374151;
        display: ${bubbleAlignment === "horizontal" ? "none" : "block"};
      }

      .outgoing .chatbot__user__name {
        color: #3b82f6;
      }

     
      #chatbot__conversation::-webkit-scrollbar {
        width: 6px;
      }

      .chat__bubble___text {
        background-color: ${getColor(buddleColor, buddleColorShade)} !important;
        color: ${getColor(textColor, textColorShade)} !important;
      }

      #chatbot__conversation::-webkit-scrollbar-thumb {
        background: rgba(0, 0, 0, 0.2); /* color of the scrollbar thumb */
        border-radius: 10px;
        cursor: pointer;
      }

      .outgoing .chat__bubble___header {
        flex-direction: row-reverse;
      }

      .outgoing .chat__bubble___text {
        display: flex;
        justify-content: end;
        /* margin-right: 20px; */
      }

      .chat__bubble .chat__bubble___text {
        word-wrap: break-word;
        overflow-wrap: break-word;
        word-break: break-all;

        margin-left:${bubbleAlignment === "horizontal" ? "0.5rem" : "0"};
        border-radius: 0.5rem;
        padding: 0.5rem;
        font-size: 0.875rem;
        color: #4b5563;
        background-color: #ffffff;
        border: ${bubbleBorder === "true" ? "1px solid #e5e7eb;" : "none;"}
        box-shadow: ${
          bubbleBoxShadow === "inner"
            ? "inset gray 0px 0px 20px -14px;"
            : bubbleBoxShadow === "outer" && "0 1px 2px rgba(0, 0, 0, 0.1);"
        }
      }

      /* .chatbot .outgoing {
        margin: 20px 0;
        justify-content: flex-end;
      } */

      .chatbot .chat-input {
        display: flex;
        align-items: center; /* items-center */
        justify-content: space-between; /* justify-between */
        gap: 0.5rem; /* gap-2 */
        background-color: #ffffff; /* bg-white */
        padding-left: 1.25rem; /* px-5 */
        padding-right: 1.25rem; /* px-5 */
      }
      /* .chatbot .chat-input {
        position: absolute;
        bottom: 0;
        width: 100%;
        display: flex;
        gap: 5px;
        background: #fff;
        border-top: 1px solid #ccc;
      } */

      .chat-input input {
        width: 100%; /* w-full */
        border-radius: 0.5rem; /* rounded-lg */
        background-color: #ffffff; /* bg-white */
        padding: 0.5rem; /* p-2 */
        color: #4b5563; /* text-gray-600 */
        outline: none;
        border: none;
        height: 40px;
        font-size: 16px;
      }

      .chat-input input::placeholder {
        color: #4b5563;
        opacity: 50%;
      }

      /*.chat-input svg {
        align-self: flex-end;
        cursor: pointer;
        height: 30px;
        display: flex;
        align-items: center;
        margin-bottom: 15px;
        font-size: 1.35rem;
      } */

      @media (max-width: 490px) {
        .chatbot {
          right: 0;
          bottom: 0;
          height: 100%;
          border-radius: 0;
          width: 100%;
        }
        .chatbot .chatbox {
          height: 90%;
        }
      }

      .loading__message {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        padding-left: 1rem;
        padding-right: 1rem;
        margin-left: 1.25rem;
        border-radius: 0.75rem;
        font-size: 0.875rem;
        line-height: 1.25rem;
        overflow-wrap: break-word;
        background: transparent;
        max-width: 80%;
      }

      .chat__title_p {
        max-width: 95%;
        margin-top: 10px;
      }

      #card {
        color: #dfcaca;
        margin: 0;
        display: flex;
        justify-content: center;
        align-items: center;
      }

      #card_body {
        background: #eeeded;
        border-radius: 10px;
        height: auto;
        width: 250px;
        overflow: hidden;
      }

      #card_img {
        min-height: 120px;
        height: 135px;
        display: flex;
        justify-content: center;
        align-items: center;
        background: #b8b4b4;
        margin: 10px 10px 0px 10px;
        border-radius: 10px 10px 0px 0px;
        overflow: hidden;
      }

      #product_img {
        max-width: auto;
        max-height: 100%;
      }

      #card_text {
        color: black;
        margin: 0px 10px 10px 10px;
        background: #ffffff;
        padding-left: 10px;
        padding-right: 10px;
        overflow: hidden;
        height: auto;
        border-radius: 0px 0px 10px 10px;
      }

      a {
        color: #724ae8;
        text-decoration: none;
      }

      a:hover {
        color: #724ae8;
        text-decoration: underline;
      }

      .loader {
        width: 50px;
        aspect-ratio: 2;
        --_g: no-repeat radial-gradient(circle closest-side, #6366f1 90%, #0000);
        background: var(--_g) 0% 50%, var(--_g) 50% 50%, var(--_g) 100% 50%;
        background-size: calc(100% / 3) 50%;
        animation: l3 1s infinite linear;
      }
      @keyframes l3 {
        20% {
          background-position: 0% 0%, 50% 50%, 100% 50%;
        }
        40% {
          background-position: 0% 100%, 50% 0%, 100% 50%;
        }
        60% {
          background-position: 0% 50%, 50% 100%, 100% 0%;
        }
        80% {
          background-position: 0% 50%, 50% 50%, 100% 100%;
        }
      }
`;
document.head.appendChild(style);

let qustions = "";

async function getChatbotById(id) {
  try {
    const response = await fetch(
      `https://chatbot-server.sense-23.com/api/chatbot/${id}`
    );
    const data = await response.json();

    let qustions = ``;
    if (data) {
      data?.sample_qustion?.map((qustion) => {
        qustions += `<button
        onclick="handleChatResponse(document.querySelector('.chat-input input').value = '${qustion.text}')"
        style="width: 100%; margin-bottom: 5px; background: transparent; border-radius: 5px; border: 1px solid hsl(214.3 31.8% 91.4%); padding-top: 5px; padding-bottom: 5px; cursor: pointer;">${qustion.text}</button>`;
      });
    }
    document.getElementById("chatbot__sample_qustion").innerHTML = qustions;
  } catch (error) {
    console.error(error);
  }
}

getChatbotById(chatbot_id);

let session_id = null;
// document.addEventListener("DOMContentLoaded", function () {
//   const introductoryMessage = document.createElement("li");
//   introductoryMessage.classList.add("chat", "incoming");
//   introductoryMessage.innerHTML = `
//       <div class="message" style>
//         <img src="./nikles-image.png" style="width: 60%; display: block; margin: 40px auto " alt="logo">
//         <h3 class="chat__title" style="color: #302F2E; display: block; margin: 5px auto 0;  text-align: center;">Welcome to Nikles Chat Bot</h3>
//         <p class="chat__title" style="background-color: #fff; color: #585979; display: block; margin: 20px auto 5px;  text-align: center; padding: 6px 10px;">Please ask anything about the company and products.</p>
//       </div>
//     `;
//   const chatbox = document.querySelector(".chatbox");
//   chatbox.appendChild(introductoryMessage);
// });

const chatInput = document.querySelector(".chat-input input");
const sendChatBtn = document.getElementById("send-btn");
const chatbox = document.querySelector("#chatbot__conversation");
const chatbotToggle = document.querySelector(".chatbot-toggler");

let userMessage;
const createChatLi = (message, className) => {
  const chatLi = document.createElement("div");
  chatLi.classList.add("chat__bubble", className);

  if (className === "outgoing") {
    chatLi.classList.add("outgoing");
    const html = `<div class="outgoing chat__bubble">
            <div class="chat__bubble___header">
              <svg
                width="15"
                height="15"
                viewBox="0 0 15 15"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M7.5 0.875C5.49797 0.875 3.875 2.49797 3.875 4.5C3.875 6.15288 4.98124 7.54738 6.49373 7.98351C5.2997 8.12901 4.27557 8.55134 3.50407 9.31167C2.52216 10.2794 2.02502 11.72 2.02502 13.5999C2.02502 13.8623 2.23769 14.0749 2.50002 14.0749C2.76236 14.0749 2.97502 13.8623 2.97502 13.5999C2.97502 11.8799 3.42786 10.7206 4.17091 9.9883C4.91536 9.25463 6.02674 8.87499 7.49995 8.87499C8.97317 8.87499 10.0846 9.25463 10.8291 9.98831C11.5721 10.7206 12.025 11.8799 12.025 13.5999C12.025 13.8623 12.2376 14.0749 12.5 14.0749C12.7623 14.075 12.975 13.8623 12.975 13.6C12.975 11.72 12.4778 10.2794 11.4959 9.31166C10.7244 8.55135 9.70025 8.12903 8.50625 7.98352C10.0187 7.5474 11.125 6.15289 11.125 4.5C11.125 2.49797 9.50203 0.875 7.5 0.875ZM4.825 4.5C4.825 3.02264 6.02264 1.825 7.5 1.825C8.97736 1.825 10.175 3.02264 10.175 4.5C10.175 5.97736 8.97736 7.175 7.5 7.175C6.02264 7.175 4.825 5.97736 4.825 4.5Z"
                  fill="currentColor"
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                ></path>
              </svg>
              <span class="chatbot__user__name">Jacob Jones</span>
              <span></span>
            </div>
            <div style="display: flex; justify-content: end">
              <p class="chat__bubble___text">
                <span
                  >${message}</span
                >
              </p>
            </div>
            
          </div>`;

    chatLi.innerHTML = html;
    if (session_id == null) {
      session_id = crypto.randomUUID();
    }
  } else {
    const html = `<div class="incoming chat__bubble">
            <div class="chat__bubble___header">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                aria-hidden="true"
                data-slot="icon"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M8.25 3v1.5M4.5 8.25H3m18 0h-1.5M4.5 12H3m18 0h-1.5m-15 3.75H3m18 0h-1.5M8.25 19.5V21M12 3v1.5m0 15V21m3.75-18v1.5m0 15V21m-9-1.5h10.5a2.25 2.25 0 0 0 2.25-2.25V6.75a2.25 2.25 0 0 0-2.25-2.25H6.75A2.25 2.25 0 0 0 4.5 6.75v10.5a2.25 2.25 0 0 0 2.25 2.25Zm.75-12h9v9h-9v-9Z"
                ></path>
              </svg>
              <span class="chatbot__user__name">Bot</span>
              <span></span>
            </div>
            <div style="display: flex; justify-content: start">
            <div class="chat__bubble___text">
              <p >
                <span>
                  </span>
              </p>
              <div class="loader"></div>
              <div class='chatbot__feedback'></div>
              </div>
              
            </div>
          </div>`;

    chatLi.innerHTML = html;
    chatLi.classList.add("generating_message");
  }
  return chatLi;
};

const generateResponse = async (callback) => {
  const API_URL = "http://localhost:8000/api/chatbot/chat";
  const requestBody = {
    // question: userMessage,
    // // session_id: session_id,
    // token: session_id,
    // chatbot_id: "34",
    question: userMessage,
    chatbot_id: chatbot_id,
    token: chatbot_id,
    user_id: user_id,
  };
  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(requestBody),
  };
  const response = await fetch(API_URL, requestOptions);
  const contentType = response.headers.get("Content-Type");
  if (contentType && contentType.includes("application/json")) {
    const responseData = await response.json();
    callback(responseData);
  } else {
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let chatMessage = ``;
    while (true) {
      const { value, done } = await reader.read();

      if (done) {
        break;
      }
      let decodedChunk = decoder.decode(value, { stream: true });
      let chunkData = decodedChunk
        .trim()
        .replace(/data: /g, "")
        .replace(/"/g, "")
        .replace(/^"/, "")
        .replace(/"$/, "")
        .replace(/\\u/g, "");
      chatMessage += chunkData;
      callback(chatMessage);
    }
  }
};

const handleJsonResponse = (jsonData) => {
  const cardContainer = document.createElement("div");
  cardContainer.classList.add("card");

  cardContainer.innerHTML = `
  <div style="display: flex;">
  <svg width="10px" height="10px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path fill-rule="evenodd" clip-rule="evenodd" d="M14 8C15.1046 8 16 8.89543 16 10V14C16 15.1046 15.1046 16 14 16H10C8.89543 16 8 15.1046 8 14V10C8 8.89543 8.89543 8 10 8H14ZM13 10C13.5523 10 14 10.4477 14 11V13C14 13.5523 13.5523 14 13 14H11C10.4477 14 10 13.5523 10 13V11C10 10.4477 10.4477 10 11 10H13Z" fill="#0F0F0F"/>
  <path fill-rule="evenodd" clip-rule="evenodd" d="M11 2C11 1.44772 11.4477 1 12 1C12.5523 1 13 1.44772 13 2V4H15V2C15 1.44772 15.4477 1 16 1C16.5523 1 17 1.44772 17 2V4C18.6569 4 20 5.34315 20 7H22C22.5523 7 23 7.44771 23 8C23 8.55229 22.5523 9 22 9H20V11H22C22.5523 11 23 11.4477 23 12C23 12.5523 22.5523 13 22 13H20V15H22C22.5523 15 23 15.4477 23 16C23 16.5523 22.5523 17 22 17H20C20 18.6569 18.6569 20 17 20V22C17 22.5523 16.5523 23 16 23C15.4477 23 15 22.5523 15 22V20H13V22C13 22.5523 12.5523 23 12 23C11.4477 23 11 22.5523 11 22V20H9V22C9 22.5523 8.55229 23 8 23C7.44771 23 7 22.5523 7 22V20C5.34315 20 4 18.6569 4 17H2C1.44772 17 1 16.5523 1 16C1 15.4477 1.44772 15 2 15H4V13H2C1.44772 13 1 12.5523 1 12C1 11.4477 1.44772 11 2 11H4V9H2C1.44772 9 1 8.55229 1 8C1 7.44771 1.44772 7 2 7H4C4 5.34315 5.34315 4 7 4V2C7 1.44772 7.44771 1 8 1C8.55229 1 9 1.44772 9 2V4H11V2ZM17 6C17.5523 6 18 6.44772 18 7V17C18 17.5523 17.5523 18 17 18H7C6.44771 18 6 17.5523 6 17V7C6 6.44771 6.44772 6 7 6H17Z" fill="#5F5A5A"/>
</svg>
    <div>
    ${jsonData?.map((data) => {
      return `<div id="card">
      <div id="card_body">
        <div id="card_img">
          <img id="product_img" src="${data.image_url}" alt="image" />
        </div>
        <div id="card_text">
          <div>
            <b><a href="${data.url}">${data.name}</a></b><br>
            ${data.code}
          </div>
          <div style="margin-top: 10px">
            ${data.description}
          </div>
        </div>
      </div>
    </div>`;
    })}
    
  `;

  var lastElement = document.querySelector(".generating_message:last-child");
  lastElement.style.display = "none";

  // Removing the last element with class 'generating_message' from the DOM
  lastElement.parentNode.removeChild(lastElement);

  const chatLi = document.createElement("div");
  chatLi.classList.add("chat", "incoming");
  chatLi.appendChild(cardContainer);
  if (session_id == null) {
    session_id = crypto.randomUUID();
  }
  chatbox.appendChild(chatLi);
  chatbox.scrollTo(0, chatbox.scrollHeight);
};

const handleChatResponse = (chatMessage) => {
  userMessage = chatMessage;
  if (!userMessage) return;
  const welcomeMessage = document.getElementById("chatbot__welcome_animation");
  if (welcomeMessage) {
    welcomeMessage.style.display = "none";
  }

  chatbox.appendChild(createChatLi(chatMessage, "outgoing"));

  chatInput.value = "";

  let chatLi = createChatLi("", "incoming");

  chatLi.cloneNode(true);
  chatbox.appendChild(chatLi);
  chatbox.scrollTo(0, chatbox.scrollHeight);

  function isStringArray(str) {
    return /^\[.*\]$/.test(str);
  }

  const replaceURLsWithLinks = (text) => {
    // Regular expression to match URLs and email addresses
    const urlAndEmailRegex =
      /(?:https?|ftp):\/\/[\n\S]+|\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g;
    return text.replace(urlAndEmailRegex, (match) => {
      // Check if the match is an email address
      if (match.includes("@")) {
        // If it's an email, format with mailto:
        return `<a href="mailto:${match}">${match}</a>`;
      } else {
        // If it's a URL, format as usual
        return `<a href="${match}" target="_blank">${match}</a>`;
      }
    });
  };

  generateResponse((responseData) => {
    chatLiLoader = chatbox.querySelector(".loader");
    if (chatLiLoader) {
      chatLiLoader.classList.remove("loader");
    }
    if (isStringArray(responseData)) {
      responseData = JSON.parse(responseData);
      handleJsonResponse(responseData);
    } else {
      responseData = responseData.replace(/\\n/g, "<br>");

      chatLi.querySelector("p").innerHTML = replaceURLsWithLinks(
        responseData.replace(/\n/g, "").replace(/\n\n/g, "")
      );

      if (isFeedbackActive) {
        chatLi.querySelector(
          ".chatbot__feedback"
        ).innerHTML = `<div style="margin-top: 12px; display: flex; gap: 4px;">
            <svg style="height: 16px;" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                <path fill="currentColor" fill-rule="evenodd" d="M7 5a3 3 0 0 1 3-3h9a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-2v2a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3h2zm2 2h5a3 3 0 0 1 3 3v5h2a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1h-9a1 1 0 0 0-1 1zM5 9a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h9a1 1 0 0 0 1-1v-9a1 1 0 0 0-1-1z" clip-rule="evenodd"></path>
            </svg>
            <svg style="height: 16px;" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" transform="rotate(180)">
                <path fill="currentColor" fill-rule="evenodd" d="M11.873 21.496a1 1 0 0 1-.992.496l-.454-.056A4 4 0 0 1 7.1 16.79L7.65 15h-.718c-2.637 0-4.553-2.508-3.859-5.052l1.364-5A4 4 0 0 1 8.296 2h9.709a3 3 0 0 1 3 3v7a3 3 0 0 1-3 3h-2c-.26 0-.5.14-.628.364zM14.005 4h-5.71a2 2 0 0 0-1.929 1.474l-1.363 5A2 2 0 0 0 6.933 13h2.072a1 1 0 0 1 .955 1.294l-.949 3.084a2 2 0 0 0 1.462 2.537l3.167-5.543a2.72 2.72 0 0 1 1.364-1.182V5a1 1 0 0 0-1-1m3 9V5c0-.35-.06-.687-.171-1h1.17a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1z" clip-rule="evenodd"></path>
            </svg>

            <svg style="height: 16px;" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                <path fill="currentColor" fill-rule="evenodd" d="M11.873 21.496a1 1 0 0 1-.992.496l-.454-.056A4 4 0 0 1 7.1 16.79L7.65 15h-.718c-2.637 0-4.553-2.508-3.859-5.052l1.364-5A4 4 0 0 1 8.296 2h9.709a3 3 0 0 1 3 3v7a3 3 0 0 1-3 3h-2c-.26 0-.5.14-.628.364zM14.005 4h-5.71a2 2 0 0 0-1.929 1.474l-1.363 5A2 2 0 0 0 6.933 13h2.072a1 1 0 0 1 .955 1.294l-.949 3.084a2 2 0 0 0 1.462 2.537l3.167-5.543a2.72 2.72 0 0 1 1.364-1.182V5a1 1 0 0 0-1-1m3 9V5c0-.35-.06-.687-.171-1h1.17a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1z" clip-rule="evenodd"></path>
            </svg>
        </div>`;
      }

      chatbox.scrollTo(0, chatbox.scrollHeight);
    }
  });

  return false;
};

const handleChat = async (event) => {
  event.preventDefault();

  handleChatResponse(chatInput.value.trim());
};

sendChatBtn.addEventListener("click", handleChat);
chatInput.addEventListener("keydown", function (e) {
  if (e.key === "Enter") {
    e.preventDefault();
    var clickEvent = new MouseEvent("click", {
      bubbles: true,
      cancelable: true,
      view: window,
    });
    sendChatBtn.dispatchEvent(clickEvent);
  }
});

// document.querySelector("body").classList.add("show-chatbot");

// const overlay = document.querySelector(".chatbot__overlay");
// overlay.addEventListener("click", () => {
//   alert("overlay clicked");
//   const chatbox = document.querySelector(".chatbox");
//   session_id = null;
//   chatbox.innerHTML = "";
//   document.body.classList.remove("show-chatbot");
// });

chatbotToggle.addEventListener("click", () => {
  const chatbox = document.querySelector(".chatbox");

  if (document.body.classList.contains("show-chatbot")) {
    session_id = null;
    document.getElementById("chatbot__conversation").innerHTML = "";
    document.body.classList.remove("show-chatbot");

    const welcomeMessage = document.getElementById(
      "chatbot__welcome_animation"
    );
    if (welcomeMessage) {
      welcomeMessage.style.display = "none";
    }
  } else {
    document.body.classList.add("show-chatbot");
    getChatbotById(chatbot_id);

    const welcomeMessage = document.getElementById(
      "chatbot__welcome_animation"
    );
    if (welcomeMessage) {
      welcomeMessage.style.display = "block";
    }
  }
});
