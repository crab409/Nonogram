from tkinter import messagebox
import tkinter 
#import manu -> 서로가 서로를 참조하는 순환오류 발생! 식겁했네;;
import fun 

clickedCounter = None
lineCounter = None
board = None

def btnClicked(
    row, rowHintLabelList, 
    col, colHintLabelList,
    btn, lineAnswerCounter,
    solutionBtnCounter, 
    answerTable, app
) :
    global clickedCounter
    global lineCounter
    global board
    

    print(f"{row}행 {col}열의 버튼이 클릭됨")

    #보드의 상태를 업데이트 하는 코드 
    # 0: 선택 안됨
    # 1: 선택 됨
    # 2: 제외 됨
    board[row][col] = (board[row][col] + 1) if (board[row][col] <= 1) else (0)
    print(f"{row}열 col행에 저장된 데이터: {board[row][col]}")
    

    print("보드 상태: ")
    for line in board :
        for data in line : 
            print(data, end=' ')
        print()

    if(board[row][col] == 0) :
        btn.config(text=' ')

    elif(board[row][col] == 1) :  
        btn.config(bg="#2E2E2E")
        clickedCounter += 1
        lineCounter[0][row] += 1
        lineCounter[1][col] += 1
        
    else :  
        btn.config(bg="#F0F0F0", text='X')
        clickedCounter -= 1
        lineCounter[0][row] -= 1
        lineCounter[1][col] -= 1

    print(f"{row}열의 선택된 블록 갯수: {lineCounter[0][row]}")
    if(lineAnswerCounter[0][row] <= lineCounter[0][row]) :
        rowHintLabelList[row].config(fg="#A4A4A4")
    else :
        rowHintLabelList[row].config(fg="#151515")
    
    print(f"{col}행의 선택된 블록 갯수: {lineCounter[1][col]}")
    if(lineAnswerCounter[1][col] <= lineCounter[1][col]) :
        colHintLabelList[col].config(fg="#A4A4A4")
    else : 
        colHintLabelList[col].config(fg="#151515")

    print(f"총 {clickedCounter}개의 블럭이 선택됨. 정답 블럭의 갯수는 {solutionBtnCounter}")
    if(clickedCounter == solutionBtnCounter) :
        if(fun.is_clear(board, answerTable)) : 
            messagebox.showinfo("Congratulations!","You've solved the puzzle!")
            app.destroy()

    print('\n')

def mainGame(
    answerTable,
    tableSize,
    rowHints, colHints,
    lineAnswerCounter,
    solutionBtnCounter
) : 
    global clickedCounter
    global lineCounter
    global board 

    lineCounter = [[0 for i in range(0, tableSize[1], 1)], [0 for i in range(0, tableSize[0], 1)]]
    board = [[0 for i in range(0, tableSize[0], 1)]for j in range(0, tableSize[1], 1)]
    clickedCounter = 0
    

    print("보드 초기화됨")
    for line in board :
        for data in line : 
            print(data, end=' ')
        print()

    app = tkinter.Tk() 
    app.title("Nonogram | main game")
    app.resizable(False, False)

    rowHintLabelList = []
    for i in range(0, tableSize[1], 1) :
        rowHintLabels = tkinter.Label(app, text=rowHints[i], anchor='e', height=2, width=4, font=("Arial", 15))
        rowHintLabels.grid(row=(i+1), column=0, padx=2, pady=2, ipadx=6, ipady=2)
        rowHintLabelList.append(rowHintLabels)

    colHintLabelList = []
    for i in range(0, tableSize[0], 1) :
        colHintLabels = tkinter.Label(app, text=colHints[i], anchor='s', height=2, width=4, font=("Arial", 15))
        colHintLabels.grid(row=0, column=(i+1), padx=2, pady=2, ipadx=2, ipady=8)
        colHintLabelList.append(colHintLabels)

    for i in range(0, tableSize[1], 1) :
        for j in range(0, tableSize[0], 1) :
            btn = tkinter.Button(app, text=' ', height=3, width=6)

            btn.config(command=lambda row=i, rowHintLabelList= rowHintLabelList, 
            col=j, colHintLabelList= colHintLabelList,
            btn=btn, lineAnswerCounter= lineAnswerCounter,
            solutionBtnCounter= solutionBtnCounter,
            answerTable= answerTable, app= app: 

            btnClicked(
                row, rowHintLabelList, 
                col, colHintLabelList,
                btn, lineAnswerCounter,
                solutionBtnCounter,
                answerTable, app
            ))

            btn.grid(row=i+1, column=j+1)

    app.mainloop()