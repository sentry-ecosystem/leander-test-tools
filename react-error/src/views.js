import * as Sentry from "@sentry/react";

/**
 * A collection model that supports updating from polled data.
 */
class CollectionModel {
  constructor(data = {}) {
    this.attributes = { ...data };
    this.id = data.id || null;
  }

  updateFrom(newData) {
    Object.assign(this.attributes, newData);
  }

  get(attr) {
    return this.attributes[attr];
  }

  toJSON() {
    return { ...this.attributes };
  }
}

/**
 * A simple collection that stores models keyed by ID.
 */
class Collection {
  constructor(models = []) {
    this.models = models.map(
      (m) => (m instanceof CollectionModel ? m : new CollectionModel(m))
    );
  }

  get(id) {
    return this.models.find((m) => m.id === id) || null;
  }

  add(data) {
    const model = new CollectionModel(data);
    this.models.push(model);
    return model;
  }

  toJSON() {
    return this.models.map((m) => m.toJSON());
  }
}

/**
 * RealtimePollingView — polls a URL at a set interval and updates a
 * backing collection with the response data.
 *
 * Usage:
 *   const view = new RealtimePollingView({
 *     realtime: true,
 *     pollUrl: '/api/events/latest/',
 *     pollInterval: 3000,
 *     collection: new Collection(initialData),
 *   });
 *   view.startPolling();
 */
class RealtimePollingView {
  constructor(options = {}) {
    this.options = options;
    this.collection = options.collection || new Collection();
    this.pollInterval = options.pollInterval || 3000;
    this.pollUrl = options.pollUrl || null;
    this.realtime = options.realtime || false;
    this._timerId = null;
    this.onPollSuccess = options.onPollSuccess || null;
    this.onPollError = options.onPollError || null;
  }

  startPolling() {
    if (!this.realtime || !this.pollUrl) {
      return;
    }
    this.poll();
  }

  poll() {
    const transaction = Sentry.startTransaction({ name: "poll-update" });

    fetch(this.pollUrl)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Poll request failed: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        this._processPollData(data);
        if (this.onPollSuccess) {
          this.onPollSuccess(data);
        }
      })
      .catch((err) => {
        Sentry.captureException(err);
        if (this.onPollError) {
          this.onPollError(err);
        }
      })
      .finally(() => {
        transaction.finish();
        this._timerId = window.setTimeout(this.poll.bind(this), this.pollInterval);
      });
  }

  _processPollData(data) {
    const items = Array.isArray(data) ? data : [data];
    for (const item of items) {
      const existing = this.collection.get(item.id);
      if (existing) {
        existing.updateFrom(item);
      } else {
        this.collection.add(item);
      }
    }
  }

  stopPolling() {
    if (this._timerId !== null) {
      window.clearTimeout(this._timerId);
      this._timerId = null;
    }
  }

  destroy() {
    this.stopPolling();
    this.collection = null;
  }
}

export { CollectionModel, Collection, RealtimePollingView };
