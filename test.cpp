//time
//os
//threading
//re
#include <iostream>
#include <chrono>
#include <ctime>
using namespace std;
#include <string>
//#include <thread>

void clear()
{
  //cout << "\033[2J\033[1;1H";
}

class pipe
{
  public:
    int volume;
    float fluid;
    float flowrate;
    int position;
    int connections[1];
};


int main(int argc, char const *argv[])
{
  pipe pipes[3];

  pipes[0].volume = 60;
  pipes[0].fluid = 60;
  pipes[0].flowrate = 1;
  pipes[0].position = 3;
  pipes[0].connections[0] = 2;

  pipes[1].volume = 60;
  pipes[1].fluid = 0;
  pipes[1].flowrate = 1;
  pipes[1].position = 2;
  pipes[1].connections[0] = 2;  

  pipes[2].volume = 50;
  pipes[2].fluid = 0;
  pipes[2].flowrate = 1;
  pipes[2].position = 1;
  pipes[2].connections[0] = 0;

  bool loop = true;
  int n = 0;
  int total_fluid = 0;
  int num_equals;
  int current_sum;
  int real_total_fluid = 0;
  int fluid_error;
  bool first;
  float dtime;

  auto toc = chrono::system_clock::now();

  for (pipe p : pipes) {real_total_fluid += p.fluid;}

  while (loop)
  {
    //cout << "entered main while loop" << endl;
    dtime = 0;
    auto tic = chrono::system_clock::now();
    
    if (first)
    {
      first = false;
      toc = tic;
    }
        
    //cout << "tic variable has been initialised, printing before dtime calculation" << endl;
    chrono::duration<double> elapsed_seconds = tic-toc;
    dtime = elapsed_seconds.count();
    //cout << "dtime calculation has taken place" << endl;
    total_fluid = 0;
    n = 0;

    int ofluid[3];
    int nfluid[3];
    for (int i = 0; i < 3; i++)
    {
      ofluid[i] = 0;
      nfluid[i] = 0;
    }
    //cout << "ofluid and nfluid arrays initialised." << endl;
    for (pipe p : pipes)
    {
      //cout<<" "<<p.volume<<" "<<p.fluid<<" "<<p.flowrate<<" "<<p.position<<" "<<p.connections << endl;
      ofluid[n] = p.fluid;
      if (p.fluid > 0)
      {
        int valid_cons = 0;

        for (int d : p.connections)
        {
          if (pipes[d].fluid != pipes[d].volume) {valid_cons++;}
        }

        p.fluid += p.flowrate * valid_cons * dtime;

      if (p.fluid > p.volume) {p.fluid = p.volume;}
      if (p.fluid < 0) {p.fluid = 0;}

      for (int i : p.connections)
      {
        pipe c = pipes[i];
        if (c.position < p.position)
        {
          if (p.flowrate > 0) {c.fluid += p.flowrate * dtime;}
          if (c.fluid > c.volume) {c.fluid = c.volume;}
          if (c.fluid < 0) {c.fluid = 0;}
        }
      }

      }
      nfluid[n] = p.fluid;
      num_equals = 0;
      current_sum = 0;

      for (int i = 0; i < 100; i++)
      {
        if (ofluid[i] == nfluid[i]) {num_equals++;}
      }

      n++;
      total_fluid += p.fluid;

    }
    //cout << "main fluid logic has been done, error calculation is next" << endl;

    fluid_error = real_total_fluid - total_fluid;
    if (num_equals == 100)
    {
      cout << "nothing has changed" << endl;
      if (fluid_error != 0)
      {
        for (pipe t : pipes)
        {
          if (t.fluid != 0) {t.fluid += fluid_error;}
        }
      }
    }

    //cout << "reached the end of fluid logic";
    auto toc = chrono::system_clock::now();


    //debug stuff
    clear();
    cout << "dtime: " << dtime << endl;
    for (pipe p : pipes)
    {
      cout << "volume: " << p.volume<< " | fluid: " << p.fluid << " | flowrate: " << p.flowrate << " | position: " << p.position << " | connections: " << p.connections << endl;
    }
    cout << "total fluid in the system: " << total_fluid << " | real total fluid in the system: " << real_total_fluid << " | error in fluid calculations: " << fluid_error << endl;

  }
  
  /*/
  cout << "Hello World!";
  clear();
  return 0;
  /*/
}

