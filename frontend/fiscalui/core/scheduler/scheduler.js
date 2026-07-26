export default class Scheduler {
    constructor() {
        this._tasks = new Map();
        this._id = 0;
        this._rafId = null;
        this._frameCallbacks = [];
        this._microTasks = [];
        this._running = false;
    }

    start() {
        if (this._running) return this;
        this._running = true;
        this._loop();
        return this;
    }

    stop() {
        this._running = false;
        if (this._rafId) { cancelAnimationFrame(this._rafId); this._rafId = null; }
        return this;
    }

    setTimeout(fn, delay = 0) {
        const id = ++this._id;
        const task = { id, fn, type: 'timeout', delay, start: performance.now(), cancelled: false };
        this._tasks.set(id, task);
        return id;
    }

    setInterval(fn, interval = 1000) {
        const id = ++this._id;
        const task = { id, fn, type: 'interval', interval, start: performance.now(), lastRun: performance.now(), cancelled: false };
        this._tasks.set(id, task);
        return id;
    }

    nextFrame(fn) {
        this._frameCallbacks.push(fn);
    }

    microtask(fn) {
        this._microTasks.push(fn);
        if (this._microTasks.length === 1) queueMicrotask(() => this._flushMicrotasks());
    }

    cancel(id) {
        if (this._tasks.has(id)) this._tasks.get(id).cancelled = true;
    }

    cancelAll() {
        for (const [id] of this._tasks) this._tasks.get(id).cancelled = true;
    }

    _loop() {
        if (!this._running) return;
        this._rafId = requestAnimationFrame((time) => {
            this._processTasks(time);
            this._processFrameCallbacks();
            this._loop();
        });
    }

    _processTasks(time) {
        for (const [id, task] of this._tasks) {
            if (task.cancelled) { this._tasks.delete(id); continue; }
            if (task.type === 'timeout') {
                if (time - task.start >= task.delay) { try { task.fn(); } catch (e) { console.error('[Scheduler] timeout error', e); } this._tasks.delete(id); }
            } else if (task.type === 'interval') {
                if (time - task.lastRun >= task.interval) { try { task.fn(); } catch (e) { console.error('[Scheduler] interval error', e); } task.lastRun = time; }
            }
        }
    }

    _processFrameCallbacks() {
        const cbs = this._frameCallbacks.slice();
        this._frameCallbacks = [];
        for (const cb of cbs) try { cb(); } catch (e) { console.error('[Scheduler] frame callback error', e); }
    }

    _flushMicrotasks() {
        const tasks = this._microTasks.slice();
        this._microTasks = [];
        for (const fn of tasks) try { fn(); } catch (e) { console.error('[Scheduler] microtask error', e); }
    }

    stats() {
        return { activeTasks: this._tasks.size, frameCallbacks: this._frameCallbacks.length, microTasks: this._microTasks.length, running: this._running };
    }

    destroy() {
        this.stop();
        this._tasks.clear();
        this._frameCallbacks = [];
        this._microTasks = [];
    }
}
