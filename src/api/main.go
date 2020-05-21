package main

import (
    "fmt"
    "log"
    "net/http"
    "os"
    "os/signal"
    "time"
    "context"
    "encoding/json"
    "database/sql"
    "github.com/gorilla/mux"
    _ "github.com/go-sql-driver/mysql"
)

type Fish struct {
    Name string `json:"name"`
    ImageURI string `json:"imageURI"`
    Location string `json:"location"`
    ShadowSize int `json:"shadowSize"`
    StartTime string `json:"startTime"`
    EndTime string `json:"endTime"`
}

const (
    mysqlDriver = "mysql"
    databaseAddress = "root@tcp(127.0.0.1:3306)/nooky"
    port = ":8080"
    path = "/fishes/{name}"
    sqlStatement = "select name, imageURI, location, shadowSize, startTime, endTime from fishes where name = ?"
)

var database *sql.DB

func main() {
    log.Println("main: establishing database")
    database = establishDB()
    defer database.Close()

    log.Println("main: setting up server")
    router := setupRouter()
    server := &http.Server {
        Addr: port,
        Handler: router,
    }

    log.Println("main: running server")
    go startServer(server)

    waitForSIGINT()

    log.Println("main: shutting down")
    shutdown(server)
    os.Exit(0)
}

//establishes a handle to the db for later use
//tests a connection to nooky mysql db
func establishDB() *sql.DB {
    db, err := sql.Open(mysqlDriver, databaseAddress)
    if err != nil {
        log.Fatal(err.Error())
    }

    err = db.Ping()
    if err != nil {
        log.Fatal(err.Error())
    }

    return db
}

//setup paths to their designated handlers 
func setupRouter() *mux.Router {
    router := mux.NewRouter()
    router.HandleFunc(path, nameHandler).
        Methods("GET")

    return router
}

//handles /fishes/{name} endpoint
func nameHandler(writer http.ResponseWriter, request *http.Request) {
    name := mux.Vars(request)["name"]

    preparedStatement := prepareStatement(sqlStatement, writer)
    defer preparedStatement.Close()

    rows := queryStatement(preparedStatement, &name, writer)
    defer rows.Close()

    fish := readRow(rows, writer)
    writeFishToJSON(&fish, writer)
}

func prepareStatement(statement string, writer http.ResponseWriter) *sql.Stmt {
    preparedStatement, err := database.Prepare(statement)
    if err != nil {
        fmt.Fprintf(writer, err.Error())
    }

    return preparedStatement
}

func queryStatement(statement *sql.Stmt, name *string, writer http.ResponseWriter) *sql.Rows {
    rows, err := statement.Query(name)
    if err != nil {
        fmt.Fprintf(writer, err.Error())
    }

    return rows
}

func readRow(rows *sql.Rows, writer http.ResponseWriter) Fish {
    fish := Fish{}

    if rows.Next() {
        err := rows.Scan(&fish.Name, &fish.ImageURI, &fish.Location, &fish.ShadowSize, &fish.StartTime, &fish.EndTime)
        if err != nil {
            fmt.Fprintf(writer, err.Error())
        }
    }

    return fish
}

func writeFishToJSON(fish *Fish, writer http.ResponseWriter) {
    writer.Header().Add("Content-Type", "application/json")
    jsonWriter := json.NewEncoder(writer)
    jsonWriter.Encode(fish)
}

func startServer(server *http.Server) {
    log.Fatal(server.ListenAndServe())
}

func waitForSIGINT() {
    signalChannel := make(chan os.Signal, 1)
    signal.Notify(signalChannel, os.Interrupt) //os.Interrupt == ctrl-c
    <-signalChannel
}

func shutdown(server *http.Server) {
    waitTime := time.Second * 15 //15 seconds
    ctx, cancel := context.WithTimeout(context.Background(), waitTime)
    defer cancel()
    server.Shutdown(ctx)
}
