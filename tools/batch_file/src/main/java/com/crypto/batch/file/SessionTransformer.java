package com.crypto.batch.file;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import scala.Tuple2;

import java.text.ParseException;
import com.google.common.base.Preconditions;

public class SessionTransformer {
    private static final Logger LOGGER = LoggerFactory.getLogger(SessionTransformer.class);

    public static void main(String[] args) {
        Preconditions.checkArgument(args.length > 1,
                "Please provide the path of input file and output dir as parameters.");
        new SessionTransformer().run(args[0], args[1]);
    }

    public void run(String inputFilePath, String outputDir) {
        LOGGER.info("Run started.");

        // String master = "local[*]";
        SparkConf conf = new SparkConf()
                // .setMaster(master)
                .setAppName(SessionTransformer.class.getName());
        JavaSparkContext sc = new JavaSparkContext(conf);

        JavaRDD<String> textFile = sc.textFile(inputFilePath);
        JavaRDD<TradingSession> csvData = textFile
                .map((row) -> {
                    try {
                        return TradingSession.fromCsv(row);
                    } catch (ParseException e) {
                        return null;
                    }
                })
                .filter(row -> row != null);

        JavaPairRDD<String, String> dayState = csvData
                .mapToPair(row -> new Tuple2<>(row.date.toString(), row.getStatus()));

        dayState.saveAsTextFile(outputDir + "/dayStatus");

        sc.close();
    }
}
