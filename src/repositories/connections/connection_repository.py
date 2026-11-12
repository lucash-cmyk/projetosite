class ConnectionRepository:
    """Relacionamentos profissionais armazenados no Neo4j."""
    def __init__(self, driver, database="neo4j"):
        self._driver=driver; self._database=database
    def _run(self,query,**params):
        with self._driver.session(database=self._database) as session:
            return list(session.run(query,**params))
    def create(self,user_id,connected_user_id,data):
        rows=self._run("MERGE (a:User {id:$a}) MERGE (b:User {id:$b}) MERGE (a)-[r:CONNECTION]->(b) SET r.status=$status, r.note=$note, r.created_at=datetime() RETURN a.id AS user_id,b.id AS connected_user_id,r.status AS status,r.note AS note",a=user_id,b=connected_user_id,status=data.get("status","pending"),note=data.get("note",""))
        return dict(rows[0]) if rows else None
    def connection_exists(self,user_id,connected_user_id):
        return bool(self._run("MATCH (a:User {id:$a})-[r:CONNECTION]-(b:User {id:$b}) RETURN r LIMIT 1",a=user_id,b=connected_user_id))
    def request_connection(self,user_id,connected_user_id): return self.create(user_id,connected_user_id,{"status":"pending"})
    def list_all(self): return [dict(r) for r in self._run("MATCH (a:User)-[r:CONNECTION]->(b:User) RETURN a.id AS user_id,b.id AS connected_user_id,r.status AS status,r.note AS note")]
    def get_paginated_for_user(self,user_id,offset,limit): return [dict(r) for r in self._run("MATCH (a:User {id:$uid})-[r:CONNECTION]-(b:User) RETURN b.id AS user_id,a.id AS source_id,b.id AS target_id,r.status AS status,r.note AS note SKIP $offset LIMIT $limit",uid=user_id,offset=offset,limit=limit)]
    def update_connection_request(self,user_id,connected_user_id,data): return self.update(user_id,connected_user_id,data)
    def get_mutual_connections(self,user_id,connected_user_id): return [r["id"] for r in self._run("MATCH (a:User {id:$a})-[:CONNECTION {status:'accepted'}]-(m:User)-[:CONNECTION {status:'accepted'}]-(b:User {id:$b}) RETURN DISTINCT m.id AS id",a=user_id,b=connected_user_id)]
    def get_shortest_path(self,user_id,target_user_id):
        rows=self._run("MATCH p=shortestPath((a:User {id:$a})-[:CONNECTION*..6]-(b:User {id:$b})) RETURN [n IN nodes(p) | n.id] AS path LIMIT 1",a=user_id,b=target_user_id)
        return rows[0]["path"] if rows else []
    def count_connections(self,user_id):
        rows=self._run("MATCH (a:User {id:$uid})-[:CONNECTION {status:'accepted'}]-(b:User) RETURN count(DISTINCT b) AS total",uid=user_id); return rows[0]["total"] if rows else 0
    def update(self,user_id,connected_user_id,data):
        rows=self._run("MATCH (a:User {id:$a})-[r:CONNECTION]-(b:User {id:$b}) SET r += $data RETURN count(r) AS changed",a=user_id,b=connected_user_id,data=data); return bool(rows and rows[0]["changed"])
    def delete(self,user_id,connected_user_id):
        rows=self._run("MATCH (a:User {id:$a})-[r:CONNECTION]-(b:User {id:$b}) DELETE r RETURN count(r) AS changed",a=user_id,b=connected_user_id); return bool(rows and rows[0]["changed"])
