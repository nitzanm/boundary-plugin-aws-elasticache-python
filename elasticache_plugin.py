import boto
import boto.elasticache
import sys
import itertools

from boundary_aws_plugin.cloudwatch_plugin import CloudwatchPlugin
from boundary_aws_plugin.cloudwatch_metrics import CloudwatchMetrics


class ElasticacheCloudwatchMetrics(CloudwatchMetrics):
    def __init__(self, access_key_id, secret_access_key):
        return super(ElasticacheCloudwatchMetrics, self).__init__(access_key_id, secret_access_key, 'AWS/ElastiCache')

    def get_region_list(self):
        # Some regions are returned that actually do not support Elasticache.  Skip those.
        return [r for r in boto.elasticache.regions() if r.name not in ['cn-north-1', 'us-gov-west-1']]

    def get_entities_for_region(self, region):
        ec = boto.elasticache.connect_to_region(region.name, aws_access_key_id=self.access_key_id,
                                                aws_secret_access_key=self.secret_access_key)
        res = ec.describe_cache_clusters(show_cache_node_info=True)
        res = res['DescribeCacheClustersResponse']['DescribeCacheClustersResult']['CacheClusters']
        return itertools.chain(*(((cc, n) for n in cc['CacheNodes']) for cc in res))

    def get_entity_source_name(self, entity):
        return '%s-node%s' % (entity[0]['CacheClusterId'], entity[1]['CacheNodeId'])

    def get_entity_dimensions(self, region, entity):
        return dict(CacheClusterId=entity[0]['CacheClusterId'], CacheNodeId=entity[1]['CacheNodeId'])

    def get_metric_list(self):
        return (
            ('CPUUtilization', 'Average', 'AWS_ELASTICACHE_CPU_UTILIZATION', 0.01),
            ('SwapUsage', 'Average', 'AWS_ELASTICACHE_SWAP_USAGE'),
            ('FreeableMemory', 'Average', 'AWS_ELASTICACHE_FREEABLE_MEMORY'),
            ('NetworkBytesIn', 'Sum', 'AWS_ELASTICACHE_NETWORK_BYTES_IN'),
            ('NetworkBytesOut', 'Sum', 'AWS_ELASTICACHE_NETWORK_BYTES_OUT'),
            ('CurrConnections', 'Average', 'AWS_ELASTICACHE_REDIS_CURR_CONNECTIONS'),
            ('Evictions', 'Sum', 'AWS_ELASTICACHE_REDIS_EVICTIONS'),
            ('Reclaimed', 'Sum', 'AWS_ELASTICACHE_REDIS_RECLAIMED'),
            ('NewConnections', 'Sum', 'AWS_ELASTICACHE_REDIS_NEW_CONNECTIONS'),
            ('BytesUsedForCache', 'Average', 'AWS_ELASTICACHE_REDIS_BYTES_USED_FOR_CACHE'),
            ('CacheHits', 'Sum', 'AWS_ELASTICACHE_REDIS_CACHE_HITS'),
            ('CacheMisses', 'Sum', 'AWS_ELASTICACHE_REDIS_CACHE_MISSES'),
            ('ReplicationLag', 'Average', 'AWS_ELASTICACHE_REDIS_REPLICATION_LAG'),
            ('GetTypeCmds', 'Sum', 'AWS_ELASTICACHE_REDIS_GET_TYPE_CMDS'),
            ('SetTypeCmds', 'Sum', 'AWS_ELASTICACHE_REDIS_SET_TYPE_CMDS'),
            ('KeyBasedCmds', 'Sum', 'AWS_ELASTICACHE_REDIS_KEY_BASED_CMDS'),
            ('StringBasedCmds', 'Sum', 'AWS_ELASTICACHE_REDIS_STRING_BASED_CMDS'),
            ('HashBasedCmds', 'Sum', 'AWS_ELASTICACHE_REDIS_HASH_BASED_CMDS'),
            ('ListBasedCmds', 'Sum', 'AWS_ELASTICACHE_REDIS_LIST_BASED_CMDS'),
            ('SetBasedCmds', 'Sum', 'AWS_ELASTICACHE_REDIS_SET_BASED_CMDS'),
            ('SortedSetBasedCmds', 'Sum', 'AWS_ELASTICACHE_REDIS_SORTED_SET_BASED_CMDS'),
            ('CurrItems', 'Average', 'AWS_ELASTICACHE_REDIS_CURR_ITEMS'),
            ('BytesUsedForCacheItems', 'Average', 'AWS_ELASTICACHE_MEMCACHED_BYTES_USED_FOR_CACHE_ITEMS'),
            ('BytesReadIntoMemcached', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_BYTES_READ_INTO_MEMCACHED'),
            ('BytesWrittenOutFromMemcached', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_BYTES_WRITTEN_OUT_FROM_MEMCACHED'),
            ('CasBadval', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_CAS_BADVAL'),
            ('CasHits', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_CAS_HITS'),
            ('CasMisses', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_CAS_MISSES'),
            ('CmdFlush', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_CMD_FLUSH'),
            ('CmdGet', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_CMD_GET'),
            ('CmdSet', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_CMD_SET'),
            ('CurrConnections', 'Average', 'AWS_ELASTICACHE_MEMCACHED_CURR_CONNECTIONS'),
            ('CurrItems', 'Average', 'AWS_ELASTICACHE_MEMCACHED_CURR_ITEMS'),
            ('DecrHits', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_DECR_HITS'),
            ('DecrMisses', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_DECR_MISSES'),
            ('DeleteHits', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_DELETE_HITS'),
            ('DeleteMisses', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_DELETE_MISSES'),
            ('Evictions', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_EVICTIONS'),
            ('GetHits', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_GET_HITS'),
            ('GetMisses', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_GET_MISSES'),
            ('IncrHits', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_INCR_HITS'),
            ('IncrMisses', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_INCR_MISSES'),
            ('Reclaimed', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_RECLAIMED'),
            ('BytesUsedForHash', 'Average', 'AWS_ELASTICACHE_MEMCACHED_BYTES_USED_FOR_HASH'),
            ('CmdConfigGet', 'Average', 'AWS_ELASTICACHE_MEMCACHED_CMD_CONFIG_GET'),
            ('CmdConfigSet', 'Average', 'AWS_ELASTICACHE_MEMCACHED_CMD_CONFIG_SET'),
            ('CmdTouch', 'Average', 'AWS_ELASTICACHE_MEMCACHED_CMD_TOUCH'),
            ('CurrConfig', 'Average', 'AWS_ELASTICACHE_MEMCACHED_CURR_CONFIG'),
            ('EvictedUnfetched', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_EVICTED_UNFETCHED'),
            ('ExpiredUnfetched', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_EXPIRED_UNFETCHED'),
            ('SlabsMoved', 'Average', 'AWS_ELASTICACHE_MEMCACHED_SLABS_MOVED'),
            ('TouchHits', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_TOUCH_HITS'),
            ('TouchMisses', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_TOUCH_MISSES'),
            ('NewConnections', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_NEW_CONNECTIONS'),
            ('NewItems', 'Sum', 'AWS_ELASTICACHE_MEMCACHED_NEW_ITEMS'),
            ('UnusedMemory', 'Average', 'AWS_ELASTICACHE_MEMCACHED_UNUSED_MEMORY'),
        )


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-v':
        import logging
        logging.basicConfig(level=logging.INFO)

    plugin = CloudwatchPlugin(ElasticacheCloudwatchMetrics, 'NEM_', 'boundary-plugin-aws-elasticache-python-status')
    plugin.main()

