#include <iostream>
#include <fstream>
#include <cmath>
using namespace std;

const int datatotal = 1964;
const int utotal = 4;
const int mtotal = 491;
const int featuretotal = 10;
const int cycletotal = 150;
float learning = 0.001;
float regularization = 0.015;
float ufeatures[utotal][featuretotal];
float mfeatures[mtotal][featuretotal];
float data[datatotal][4];

void initialize() {
  ifstream f;
  int i, j, uid, mid, date, rate;
  for(i = 0;i < utotal;i++) {
    for(j = 0;j < featuretotal;j++) {
      ufeatures[i][j] = 0.1;
    } 
  }
  for(i = 0;i < mtotal;i++) {
    for(j = 0;j < featuretotal;j++) {
      mfeatures[i][j] = 0.1;
    }
  }
  f.open("ratings_transformed.txt");
  i = 0;
  if (f.is_open()) {
    while (!f.eof()) {
      f >> uid;
      f >> mid;
      f >> rate;
      data[i][0] = uid;
      data[i][1] = mid;
      data[i][2] = (float)rate;
      i++;
    }
  }
  f.close();
}

void getFeatures(int uid, int mid, float rate, float cache, int feature) {
  float rate_guess = cache + ufeatures[uid][feature] * mfeatures[mid][feature];
  float err = (float(rate) - float(rate_guess));
  ufeatures[uid][feature] += float(learning * (err * mfeatures[mid][feature] - regularization * ufeatures[uid][feature]));
  mfeatures[mid][feature] += float(learning * (err * ufeatures[uid][feature] - regularization * mfeatures[mid][feature]));
}

void setFeatures() {
  ofstream fu;
  fu.open("u_similarity_transformed.txt");
  for(int i = 0;i < utotal;i++) {
    for(int j = 0;j < utotal;j++) {
      if (i != j) {
        double error = 0.0;
        for(int k = 0;k < featuretotal;k++) {
	  error += (ufeatures[i][k] - ufeatures[j][k]) * (ufeatures[i][k] - ufeatures[j][k]);
        }
	fu << i;
        fu << " ";
        fu << j;
        fu << " ";
        fu << error;
        fu << "\n";
      }
    }
  }
  fu.close();
  ofstream fm;
  fm.open("m_similarity_transformed.txt");
  for(int i = 0;i < mtotal;i++) {
    for(int j = 0;j < mtotal;j++) {
      if (i != j) {
        double error = 0.0;
        for(int k = 0;k < featuretotal;k++) {
	  error += (mfeatures[i][k] - mfeatures[j][k]) * (mfeatures[i][k] - mfeatures[j][k]);
	}
	fm << i;
        fm << " ";
        fm << j;
        fm << " ";
        fm << error;
	fm << "\n";
      }
    }
  }
  fm.close();
  /*
  ofstream fu;
  fu.open("uid_features.txt");
  for(int m = 0;m < utotal;m++) {
    for(int n = 0;n < featuretotal;n++) {
      fu << ufeatures[m][n];
      fu << " ";
    } 
    fu << "\n";
  }
  fu.close();
  ofstream fm;
  fm.open("mid_features.txt");
  for(int m = 0;m < mtotal;m++) {
    for(int n = 0;n < featuretotal;n++) {
      fm << mfeatures[m][n];
      fm << " ";
    } 
    fm << "\n";
  } 
  fm.close();
  */
  ofstream predictions;
  predictions.open("predicted_ratings_transformed.txt");
  for(int i = 0;i < utotal;i++) {
    for(int j = 0;j < mtotal;j++) {
      double total = 0.0;
      for(int k = 0;k < featuretotal;k++) {
        total += ufeatures[i][k] * mfeatures[j][k];
      }
      if (total > 5) total = 5;
      if (total < 1) total = 1;
      predictions << i;
      predictions << " "; 
      predictions << j;
      predictions << " ";
      predictions << total;
      predictions << "\n";
    }
  }
  predictions.close();
}

int main() {
  initialize();
  for(int i = 0;i < featuretotal;i++) {
    for(int j = 0;j < cycletotal;j++) {
      for(int k = 0;k < datatotal;k++) {
        getFeatures((int)data[k][0], (int)data[k][1], data[k][2], data[k][3], i);
      }
    }
    for(int k = 0;k < datatotal;k++) {
      data[k][3] += (float)(ufeatures[(int)data[k][0]][i] * mfeatures[(int)data[k][1]][i]);
    }
  }
  setFeatures();
  return 0;
}
