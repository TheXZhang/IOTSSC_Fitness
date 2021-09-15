package com.example.iotssc;

public class Result {

    private final String time;
    private final String classification_result;

    public Result(String time, String classification_result) {
        this.time = time;
        this.classification_result = classification_result;
    }

    public String getTime() {
        return time;
    }

    public String getResult() {
        return classification_result;
    }
}
