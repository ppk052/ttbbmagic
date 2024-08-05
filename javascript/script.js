const radian=5;//const는 수정불가, let은 수정가능
let pos=[100,10];//원위치정보 in js (위,왼)
const pattern = /\((\d+),(\d+),(\d+)\)/;//받은 메세지에서 특정값 추출을 위한 정규식(그릴지여부,위,왼)
let write = true;//그릴지여부
const circle = document.querySelector("div");

localStorage.setItem("top","0");
localStorage.setItem("left","0"); //html에서 쓸 위치정보

//웹소켓연결
const webSocket = new WebSocket("ws://localhost:8000");//(1)-(1) 웹소켓 열기 // 현재는 주소가 로컬호스트로 되어있다.
webSocket.onopen = function(){           // 소켓이 열렸으면
  console.log("Web Socket Connected");   // 열렸다고 콘솔에 찍기
  webSocket.send('안녕하세요');           //(1)-(2) 서버에 메시지 보내보기
}

webSocket.onmessage = function( message ){//(3) 메시지 받았으면
  console.log( message.data );            //콘솔표시
  if(pattern.test(message.data)) 
    {
      console.log("ok");
      const info = pattern.exec(message.data);
      console.log(typeof(info[0]));
      console.log(info[1]);
      if(info[1] == "0")
      {
        circle.id = "";
        write = false;
        console.log("안보임");
      }
      else
      {
        circle.id = "visality";
        write = true;
        console.log("보임");
      }
      console.log(info[2]+"px");
      circle.style.top = info[2]+"px";
      console.log(info[3]+"px");
      circle.style.left = info[3]+"px";
    }        
}

/*const button = document.querySelector("button");
button.addEventListener("click",clicked);
function clicked(event)
{
  if(write)
  {
    circle.id = "";
    write = false;
  }
  else
  {
    circle.id = "visality";
    write = true;
  }
}
*/




