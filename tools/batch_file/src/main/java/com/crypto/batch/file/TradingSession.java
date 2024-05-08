package com.crypto.batch.file;

import java.io.Serializable;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class TradingSession implements Serializable {
    public Date date;
    public Double open;
    public Double high;
    public Double low;
    public Double close;
    public Double volume;
    public String currency;

    TradingSession(
            String date,
            String open,
            String high,
            String low,
            String close,
            String volume,
            String currency) throws ParseException {
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        this.date = dateFormat.parse(date);
        this.open = Double.parseDouble(open);
        this.high = Double.parseDouble(high);
        this.low = Double.parseDouble(low);
        this.close = Double.parseDouble(close);
        this.volume = Double.parseDouble(volume);
        this.currency = currency;
    }

    public String getStatus() {
        if (this.open < this.close)
            return "UP";
        return "DOWN";
    }

    public static TradingSession fromCsv(String row) throws ParseException {
        String[] cols = row.split(",");

        return new TradingSession(
                cols[0],
                cols[1],
                cols[2],
                cols[3],
                cols[4],
                cols[5],
                cols[6]);
    }
}
