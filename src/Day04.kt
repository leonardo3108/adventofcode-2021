import java.io.File

class Board (pSize: Int) {
    private val size: Int = pSize
    val lines = Array(size = size, init = { i -> Array(size = size, init = { i -> 0}) })
    val columnNumber = HashMap<Int, Int>()
    val lineNumber = HashMap<Int, Int>()
    var bingo = false
    val history: MutableList<Int> = arrayListOf()
    val lack: HashSet<Int> = HashSet()

    public fun addValue(x: Int, y: Int, value: Int) {
        lines[y][x] = value
        columnNumber[value] = x
        lineNumber[value] = y
        lack.add(value)
    }
    public fun markValue(value: Int): Boolean {
        if (bingo)
            return false
        if (lack.remove(value)) {
            history.add(value)
            if (checkColumn(columnNumber.get(value)!!) || checkColumn(lineNumber.get(value)!!)) {
                bingo = true
                return true
            }
        }
        return false
    }
    public fun checkLine(y: Int): Boolean {
        for (value in lines.get(y))
            if (value in lack)
                return false
        return true
    }
    public fun checkColumn(x: Int): Boolean {
        for (value in lines.get(x))
            if (value in lack)
                return false
        return true
    }
    public fun score(last: Int): Int {
        var sigma = lack.sum()
        println("\tsum(" + sigma + ") x last(" + last + ") = " + (sigma * last))
        return sigma * last
    }
}

var firstBingo = false

fun main() {
    var section = "CHOSEN"
    val BOARD_SIZE = 5
    val COLUMN_WIDTH = 3
    var boards: MutableList<Board> = arrayListOf()
    var line_nr = 0
    var board_nr = -1
    var chosenNumbers: List<String> = arrayListOf()
    File("resource/input04.txt").forEachLine {
        when (section) {
            "CHOSEN" -> {
                chosenNumbers = it.split(",")
                println(chosenNumbers)
                section = "SPACE"
            }
            "SPACE" -> {
                section = "BOARD"
                line_nr = 0
                boards.add(Board(BOARD_SIZE))
                board_nr++
            }
            "BOARD" -> {
                for (column_nr in 0..BOARD_SIZE-1) {
                    val cell = it.substring(startIndex = column_nr * COLUMN_WIDTH, endIndex = column_nr * COLUMN_WIDTH + 2).trim().toInt()
                    boards[board_nr].addValue(x = column_nr, y = line_nr, value = cell)
                }
                line_nr++
                if (line_nr == BOARD_SIZE)
                    section = "SPACE"
            }
            else -> println(it)
        }
    }
    bingo(chosenNumbers, boards)
}

private fun bingo(
    chosenNumbers: List<String>,
    boards: MutableList<Board>
) {
    for (chosenNumber in chosenNumbers) {
        var i = 0
        for (board in boards) {
            if (board.markValue(chosenNumber.toInt())) {
                println("Completed board " + i + " " + board.history + "-" + board.lack + "(" + board.lack.sum() + ")")
                boards[i].score(chosenNumber.toInt())
                firstBingo = true
            }
            i++
        }
    }
}