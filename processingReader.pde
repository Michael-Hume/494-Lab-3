import processing.serial.*;

String input;
String[] data;
FloatList heartPlot;
BufferedReader reader;
String line;

void setup(){
  size(1200, 1000);
  background(0);
  heartPlot = new FloatList();
  reader = createReader("../lab3Readings.txt");
}

void plot(){
  background(0); // clear the background for sharper lines
  
  noFill();
  stroke(227, 34, 255); // purple
  strokeWeight(1.0);
  strokeJoin(ROUND);
  fill(227, 34, 255);
  //beginShape();
  for (int i = 0; i < heartPlot.size(); i++){
    ellipse(i, height - heartPlot.get(i), 3, 3);
  }
  //endShape();
  
  noFill();
  stroke(227, 255, 255); // purple
  strokeWeight(1.0);
  strokeJoin(ROUND);
  beginShape();
  
  
  for (int i = 0; i < heartPlot.size(); i++){
    vertex(i, height - heartPlot.get(i));
  }
  endShape();
  
  if (heartPlot.size() >= width){
    background(0);
    heartPlot.clear();
  }
 
}

void draw(){
  try {
    line = reader.readLine();
    data = split(line, ',');
    StringList temp = new StringList(data);
    for(String x: temp){
      if (!Float.isNaN(float(x)))
            heartPlot.append(map(float(x), 0, 1023, 0, height));
    }
    plot();
    
    
  }
  catch (IOException e){}
  catch (Exception e){}
}
