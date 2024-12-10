import tkinter
import main
import sys
import fun
import os

#게임을 선택했을때, 실행할 함수 
def gameSelec(nowSelected, indexNumber=0) :
    global gameSelectBtnList
    global nowSelectedGameId
    global gameInfo


    needNone = nowSelectedGameId
    if (nowSelected != needNone) :
        print(f"게임 선택 변경됨 : {needNone} to {nowSelected}")

        #색상 바꾸기 알고리즘
        idx = () if () else ()
        gameSelectBtnList[needNone % 10].config(bg= "#F0F0F0")#  색상 기본으로 전환
        gameSelectBtnList[nowSelected % 10].config(bg= "#A4A4A4")#  색상 진하게 

        nowSelectedGameId = nowSelected#선택된 게임 ID 변경 
        row_num, col_num = fun.load_size(nowSelectedGameId+1)
        contents = f"table number: {nowSelectedGameId}\ntalble size: {row_num}x{col_num}"
        gameInfo.config(
            text= contents
        )


#인덱스 버튼을 클릭했을때, 실행할 함수 
def indexClicked(nowSelected) : 
    global nowSelectedIdxId

    print(f"현제 선택된 index : {nowSelectedIdxId}, 선택될 index : {nowSelected}")

    if (nowSelectedIdxId != nowSelected) : 
        global indexList
        global gameSelectBtnList
        global fileCount

        #색상 바꾸는 알고리즘 
        indexList[nowSelected].config(bg= "#A4A4A4")
        indexList[nowSelectedIdxId].config(bg= "#F0F0F0")

        nowSelectedIdxId = nowSelected

        idx = nowSelected
        nowSelecIdx = idx

        for i in range(0, 10, 1) :
            gameSelectBtnList[i].config(
                text= "",
                bd= 0,
                command=None
            )

        if (fileCount // 10 > idx) : 
            for i in range(0, 10, 1) :
                gameSelectBtnList[i].config(
                    text= f"{idx*10+i+1}. Nonogram",
                    bd= 2,
                    command=lambda idx= i + idx * 10 : gameSelec(idx)
                )
        else :
            for i in range(0, fileCount%10, 1) :
                gameSelectBtnList[i].config(
                    text= f"{idx*10+i+1}. Nonogram",
                    bd= 2,
                    command=lambda idx= i + idx * 10 : gameSelec(idx)
                )
    
def bridge() :
    global nowSelectedGameId

    row_hints, col_hints = fun.load_hints(nowSelectedGameId+1)
    print(f"행{row_hints}, 열{col_hints}")
    lineAnswer = [#분명 내가 몇주전까지만 해도 몇초만에 생각해서 뚝딱 만든건데 원리를 모르겠음;;
        [sum(i) for i in row_hints], 
        [sum(i) for i in col_hints]
    ] 
    solutionTable = fun.load_answers(row_hints, col_hints) #버그가 나는데... 고칠 엄두가 안난다... 
    print(f"manu.py: bridge함수, solutionTable:{solutionTable}")

    solutionBtnCounter = fun.count_solution(solutionTable)
    print(f"정답 개수 {solutionBtnCounter}")
    answerConuter = fun.count_solution(solutionTable)
    tableSize = [len(solutionTable[0]), len(solutionTable[1])]
    rowHints, colHints = fun.hints_to_str(row_hints, col_hints)


    main.mainGame(
        answerTable= solutionTable,
        tableSize= tableSize,
        rowHints= rowHints, colHints= colHints,
        lineAnswerCounter= lineAnswer,
        solutionBtnCounter= solutionBtnCounter
    )
    


#tables안의 파일의 갯수를 세어 fileCount변수에 저장하기
tableFolderPath = os.path.join(os.path.dirname(sys.argv[0]), "tables")
fileCount = len([file for file in os.listdir(tableFolderPath) if os.path.isfile(os.path.join(tableFolderPath, file))])
print(f"저장된 게임 개수 : {fileCount}")

#앱을 구성할 기본 설정 
app = tkinter.Tk() 
app.wm_iconbitmap('logo.ico')
app.title("Nonogram | Manu")
app.resizable(False, False)
app.geometry("500x700")


#게임 리스트의 인덱스를 나열할 인덱스 프레임 제작 
idxCount = (fileCount // 10) if (fileCount % 10 == 0) else (fileCount // 10 + 1)
print(f"게임 갯수 : {fileCount}, 인덱스 갯수 : {idxCount}")

indexFrame = tkinter.Frame(app)
indexFrame.pack(
    side= 'top',
    fill= 'x',
    ipadx=10,
    pady=10, 
    padx=10
)

nowSelectedIdxId = 0
indexList = []
for i in range(0, idxCount, 1) :
    idxBtn = tkinter.Button(
        indexFrame,
        text= f"{i+1}",
        font= ("Arial", 15),
        command= lambda idx= i : indexClicked(idx)
    )
    idxBtn.grid(row=0, column=i, padx=3)
    indexList.append(idxBtn)

indexList[0].config(bg= "#A4A4A4")




#게임 리스트를 나열할 메인 프레임 제작
mainFrame = tkinter.Frame(app)
mainFrame.pack(
    side="top",
    expand=True,
    fill="both",
    ipadx=10,
    ipady=10,
    pady=10
)

#게임 리스트 버튼 생성
nowSelectedGameId = 0
gameSelectBtnList = []
for i in range(0, 10, 1) :
    gameSelectBtn = tkinter.Button(
        mainFrame,
        anchor= 'w',
        font= ("Arial", 17),
        bd= 0
    )
    gameSelectBtn.pack(fill='x', padx=10)
    gameSelectBtnList.append(gameSelectBtn)

#게임 리스트 나열 
for i in range(0, 10 if (fileCount >= 10) else (fileCount % 10), 1) :
    gameSelectBtnList[i].config(
        text = f"{i+1}. Nonogram",
        bd= 2,
        command= lambda idx= i : gameSelec(idx)
    )

gameSelectBtnList[0].config(bg="#A4A4A4")



gameInfoFrame = tkinter.Frame(app)
gameInfoFrame.pack(side="bottom", fill='x')
contents = f"table number: 0\ntalble size: 가로x세로"
gameInfo = tkinter.Label(gameInfoFrame, text=contents, font= ("Arial", 15), justify='left')
gameInfo.grid(row= 0, column=0)
gameStartBtn = tkinter.Button(
    gameInfoFrame,
    text= "Game Start!",
    bg= "#A4A4A4",
    font= ("Arial", 15),
    command= bridge
)
gameStartBtn.grid(row= 1, column=0)


app.mainloop()