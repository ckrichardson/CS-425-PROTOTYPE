/*
 * Author: Justin A. Haghighi
 * Project: CS-425-PROTOTYPE
 * Date: 2019-12-05
 * Subject: Create a working Flink program
 * Tutorial Source: https://www.tutorialdocs.com/article/first-flink-app.html
 */
package myflink;

import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.util.Collector;
import org.apache.flink.api.java.tuple.Tuple2;

public class SocketWindowWordCount {
    @SuppressWarnings("Convert2Lambda")
    public static void main(String[] args) throws Exception {
        // "Entry class" which sets parameters, creates data sources, and submits tasks
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        /*
         *
         * Data source reads from local port 9000
         * DataStream is the core API for Stream processing in Flink and can define filtering, transformation,
         * aggregation, window, association, and more
         *
         */
        DataStream<String> text = env.socketTextStream("localhost", 9000, "\n");

        // Count the number of words that appear within a certain time window
        // flatmap maps and flattens a set of data (there may be multiple words per line)
        // Tuples are collections of objects that may or may not be related
        DataStream<Tuple2<String, Integer>> wordCounts = text
                .flatMap(new FlatMapFunction<String, Tuple2<String, Integer>>() {
                    @Override
                    public void flatMap(String value, Collector<Tuple2<String, Integer>> out) {
                        for (String word : value.split("\\s")) {
                            out.collect(Tuple2.of(word, 1));
                        }
            }
        });

        // Group data stream according to word and specify the window by which to count (5 seconds)
        DataStream<Tuple2<String, Integer>> windowCounts = wordCounts
                .keyBy(0) // keyBy(int index)
                .timeWindow(Time.seconds(5)) // Specify 5 second time window to count a word
                .sum(1); // Sum the count value on each key (word)

        windowCounts.print().setParallelism(1); // Print the data stream to the console
        env.execute("Socket Window WordCount"); // Execute the actual Flink operation
    }
}
