#ifndef SEGMENT_TREE_H
#define SEGMENT_TREE_H

#include <vector>
#include <fstream>
#include <string>
#include <sstream>


class StepLogger {
public:
    explicit StepLogger(const std::string& path) : out(path) {
        out << "[\n";
        first = true;
    }

    ~StepLogger() {
        out << "\n]\n";
        out.close();
    }

    void log(const std::string& step, int node, int start, int end,
             long long value, const std::string& extra = "") {
        if (!first) out << ",\n";
        first = false;
        out << "  {"
            << "\"op\":\"" << step << "\","
            << "\"node\":" << node << ","
            << "\"start\":" << start << ","
            << "\"end\":" << end << ","
            << "\"value\":" << value;
        if (!extra.empty()) out << "," << extra;
        out << "}";
    }

    // Marca el inicio de una operación de alto nivel (para agrupar en la animación)
    void logHeader(const std::string& opName, const std::string& paramsJson) {
        if (!first) out << ",\n";
        first = false;
        out << "  {\"op\":\"header\",\"name\":\"" << opName << "\","
            << "\"params\":" << paramsJson << "}";
    }

private:
    std::ofstream out;
    bool first;
};

class SegmentTree {
public:
    SegmentTree(const std::vector<int>& arr, StepLogger& logger)
        : n((int)arr.size()), tree(4 * (int)arr.size(), 0), log(logger) {
        if (n > 0) build(arr, 1, 0, n - 1);
    }

    void update(int idx, int val) {
        std::ostringstream params;
        params << "{\"index\":" << idx << ",\"value\":" << val << "}";
        log.logHeader("update", params.str());
        update(1, 0, n - 1, idx, val);
    }

    long long query(int l, int r) {
        std::ostringstream params;
        params << "{\"left\":" << l << ",\"right\":" << r << "}";
        log.logHeader("query", params.str());
        return query(1, 0, n - 1, l, r);
    }

private:
    int n;
    std::vector<long long> tree;
    StepLogger& log;

    void build(const std::vector<int>& arr, int node, int start, int end) {
        log.log("build_visit", node, start, end, 0);
        if (start == end) {
            tree[node] = arr[start];
            log.log("build_set", node, start, end, tree[node]);
            return;
        }
        int mid = (start + end) / 2;
        build(arr, 2 * node, start, mid);
        build(arr, 2 * node + 1, mid + 1, end);
        tree[node] = tree[2 * node] + tree[2 * node + 1];
        log.log("build_set", node, start, end, tree[node]);
    }

    void update(int node, int start, int end, int idx, int val) {
        log.log("update_visit", node, start, end, tree[node]);
        if (start == end) {
            tree[node] = val;
            log.log("update_set", node, start, end, tree[node]);
            return;
        }
        int mid = (start + end) / 2;
        if (idx <= mid) update(2 * node, start, mid, idx, val);
        else update(2 * node + 1, mid + 1, end, idx, val);
        tree[node] = tree[2 * node] + tree[2 * node + 1];
        log.log("update_set", node, start, end, tree[node]);
    }

    long long query(int node, int start, int end, int l, int r) {
        if (r < start || end < l) {
            log.log("query_out_of_range", node, start, end, 0);
            return 0;
        }
        if (l <= start && end <= r) {
            log.log("query_leaf", node, start, end, tree[node]);
            return tree[node];
        }
        log.log("query_partial", node, start, end, tree[node]);
        int mid = (start + end) / 2;
        long long leftSum = query(2 * node, start, mid, l, r);
        long long rightSum = query(2 * node + 1, mid + 1, end, l, r);
        return leftSum + rightSum;
    }
};

#endif
